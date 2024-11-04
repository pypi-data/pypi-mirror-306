import gaiaengine as gaia
import sdl2


class ImpostorSelectorInput(gaia.EventListener):
    def __init__(self, event_manager, selector):
        super().__init__(event_manager)
        self.selector = selector
        
        self.heightmap_camera = None
        self.click_to_lock_on = True
        self.lock_on_timer = None
        self.lock_on_camera_radius = 12.0
        self.lerp_time_lock_on = 0.2

        self.rotation_speed = 0.1
        self.simulate_touch = False  # If the mouse should behave the same as touch

    def start_lock_on(self, impostor, heightmap_camera):
        heightmap_camera.lockedOnImpostor = impostor
        heightmap_camera.lerpTimeMs = (int)(self.lerp_time_lock_on * 1000)
        heightmap_camera.radius = self.lock_on_camera_radius
        self.heightmap_camera = heightmap_camera
        if self.lock_on_timer is None:
            self.lock_on_timer = self.window.timer_manager.addAbsoluteTimer(gaia.Callback(self.update_lock_on), 0.0, True)

    def stop_lock_on(self):
        self.lock_on_timer.cancel()
        self.lock_on_timer = None
        self.heightmap_camera.lockedOnImpostor = None
        self.heightmap_camera = None

    def update_lock_on(self):
        locked_on_impostor = self.heightmap_camera.lockedOnImpostor

        if locked_on_impostor is None:
            self.stop_lock_on()
            return
    
        if locked_on_impostor not in self.selector.selection or not locked_on_impostor.canBeSelected:
            self.selector.removeFromSelection(locked_on_impostor)
            self.stop_lock_on()
            return
        
        # Dezooming unlocks the camera
        if self.heightmap_camera.radius != self.lock_on_camera_radius:
            self.stop_lock_on()
            return

    def is_touch_event(self, event):
        return event.motion.which == sdl2.SDL_TOUCH_MOUSEID or self.simulate_touch

    def handleEvent(self, window, event):
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.scancode == sdl2.SDL_SCANCODE_SPACE:
                window.camera.lerpTimeMs = (int)(self.lerp_time_lock_on * 1000)
                self.selector.goBackToSelection(window.camera)
                return True

            elif event.key.keysym.scancode == sdl2.SDL_SCANCODE_DELETE:
                self.selector.deleteOneInSelection()
                return True

        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            # Save the location of where dragging was started, but don't show the selection rectangle yet (see EVENT_DRAG_BEGIN)
            self.selector.selectionRectangle = gaia.iVec4(event.button.x, event.button.y, 0, 0)

            if event.button.button == sdl2.SDL_BUTTON_RIGHT:
                if not self.selector.isSelectionEmpty():
                    self.selector.moveSelection(window.camera.screenToWorldPos(gaia.iVec2(event.button.x, event.button.y)))
                    return True
                
        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
            if event.button.button == sdl2.SDL_BUTTON_LEFT and event.button.clicks == 2 and not self.is_touch_event(event):
                clicked_impostor = self.selector.getSelectableImpostor(gaia.iVec2(event.button.x, event.button.y))
                # Only select similar impostors on double click if the first click already selected the impostor
                if clicked_impostor is not None and clicked_impostor in self.selector.selection:
                    selection_rectangle = gaia.iVec4(0, 0, window.windowSize)
                    add_to_selection = sdl2.SDL_GetKeyboardState(None)[sdl2.SDL_SCANCODE_LSHIFT]
                    double_click_filter = lambda impostor : impostor.type == clicked_impostor.type and impostor.asset == clicked_impostor.asset
                    self.selector.select(selection_rectangle, add_to_selection, double_click_filter)
                    return True

        elif event.type == gaia.EVENT_CLICK:
            should_consume = False

            selectable_impostor = self.selector.getSelectableImpostor(gaia.iVec2(event.button.x, event.button.y))

            if not self.selector.isSelectionEmpty():
                if selectable_impostor is None or not sdl2.SDL_GetKeyboardState(None)[sdl2.SDL_SCANCODE_LSHIFT]:
                    self.selector.clearSelection()
                should_consume = True

            if selectable_impostor is not None:
                self.selector.addToSelection(selectable_impostor)
                should_consume = True
                if self.is_touch_event(event) or (self.click_to_lock_on and not sdl2.SDL_GetKeyboardState(None)[sdl2.SDL_SCANCODE_LSHIFT]):
                    self.start_lock_on(selectable_impostor, window.camera)
            
            return should_consume
        
        # Rotation around locked-on impostor
        if self.lock_on_timer is not None and window.camera == self.heightmap_camera:
            if event.type == gaia.EVENT_DRAG_MOTION:
                screen_rect = window.camera.lockedOnImpostor.screenRect
                # The direction of rotation depends on which quarter of the screen the cursor is
                if event.motion.x > screen_rect.x + screen_rect.z / 2:
                    window.camera.theta += event.motion.yrel * self.rotation_speed
                else:
                    window.camera.theta -= event.motion.yrel * self.rotation_speed

                if event.motion.y < screen_rect.y + screen_rect.w / 2:
                    window.camera.theta += event.motion.xrel * self.rotation_speed
                else:
                    window.camera.theta -= event.motion.xrel * self.rotation_speed

        # Handle the selection rectangle except for touch input
        elif not self.is_touch_event(event):
            if event.type == gaia.EVENT_DRAG_BEGIN:
                # Only start displaying the selection rectangle when it cannot be considered a click anymore
                self.selector.displaySelectionRectangle = True
                return True

            elif event.type == gaia.EVENT_DRAG_MOTION:
                selection_rectangle = self.selector.selectionRectangle
                selection_rectangle.z = event.motion.x - selection_rectangle.x
                selection_rectangle.w = event.motion.y - selection_rectangle.y
                self.selector.selectionRectangle = selection_rectangle
                return True

            elif event.type == gaia.EVENT_DRAG_END:
                add_to_selection = sdl2.SDL_GetKeyboardState(None)[sdl2.SDL_SCANCODE_LSHIFT]
                self.selector.select(self.selector.selectionRectangle, add_to_selection)
                self.selector.displaySelectionRectangle = False
                return True

        return False