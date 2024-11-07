import datetime
import logging
from . import _pynavlib as pynavlib

class NavlibOptions:
    NoOptions : int = 0
    NonQueuedMessages : int = 1
    RowMajorOrder : int = 2
    NoUI : int = 4
    
class NavlibTimingSource:
    SpaceMouse : int = 0
    Application : int = 1

class NavlibVector:
    
    def __init__(self, x : float = 0., y : float = 0., z : float = 0.):
        self._x = x
        self._y = y
        self._z = z

class NavlibBox:
    
    def __init__(self, box_min : NavlibVector, box_max : NavlibVector ):
        self._min = box_min
        self._max = box_max

class NavlibFrustum:
    
    def __init__(self, left : float = 0., right : float = 0.,
                       bottom : float = 0., top : float = 0.,
                       near : float = 0., far : float = 0.):
        self._left = left
        self._right = right
        self._bottom = bottom
        self._top = top
        self._near = near
        self._far = far

class NavlibMatrix:
    
    def __init__(self, matrix : list[list[float]] = [[1., 0., 0., 0.],
                                                     [0., 1., 0., 0.],
                                                     [0., 0., 1., 0.],
                                                     [0., 0., 0., 1.]]):
        self._matrix = matrix

class NavlibPlane:
    
    def __init__(self, normal : NavlibVector, distance : float = 0) :
        self._normal = normal
        self._distance = distance

class NavlibNavigationModel(pynavlib.NavlibNavigationModel):
    
    def __init__(self, multi_threaded : bool = False, navlib_options : int = 0, verbose_mode : bool = False) :
        super().__init__(multi_threaded, navlib_options)
        self._verbose_mode = verbose_mode
        logging.basicConfig(format='%(levelname)s:%(module)s:%(message)s')
    
    def get_active_commands(self)->str :
        return self._get_active_commands()
    
    def put_active_commands(self, set_id : str) :
        self._put_active_commands(set_id)
        
    def get_profile_hint(self)->str :
        return self._get_profile_hint()
    
    def put_profile_hint(self, profile_hint : str) :
        self._put_profile_hint(profile_hint)
        
    def get_frame_timing_source(self)->int :
        return self._get_frame_timing_source()
    
    def put_frame_timing_source(self, timing_source : int) :
        self._put_frame_timing_source(timing_source)

    def is_enabled(self)->bool :
        return self._is_enabled()
    
    def enable_navigation(self, enable : bool) :
        try:
            self._enable_navigation(enable)
        except RuntimeError as exc:
            logging.exception(f'enable_navigation: {type(exc)}')

    def get_frame_time(self)->datetime.timedelta :
        return self._get_frame_time()
    
    def put_frame_time(self, time : datetime.timedelta) :
        self._put_frame_time(time)

    def begin_command_set(self, command_set_id : str, command_set_name : str) :
        try:
            self._begin_command_set(command_set_id, command_set_name)
        except:
            logging.exception('begin_command_set exception: the command set is already under construction')

    def begin_command_category(self, command_category_id : str, command_category_name : str) :
        try:
            self._begin_command_category(command_category_id, command_category_name)
        except:
            logging.exception('begin_command_category exception: no command set is currently under construction')
        
    def create_command(self, command_id : str, command_name : str, command_description : str) :
        try:
            self._create_command(command_id, command_name, command_description)
        except:
            logging.exception('create_command exception: no command set is currently under construction')

    def end_command_category(self):
        try:
            self._end_command_category()
        except:
            logging.exception('end_command_category exception: no command set is currently under construction')
        
    def end_command_set(self):
        try:
            self._end_command_set()
        except:
            logging.exception('end_command_set exception: no command set is currently under construction')
        

    # Navlib interface
    
    def get_pointer_position(self) -> NavlibVector : ...
    
    def get_view_extents(self) -> NavlibBox : ...

    def get_view_fov(self) -> float : ...
    
    def get_view_frustum(self) -> NavlibFrustum : ...
    
    def get_is_view_perspective(self) -> bool : ...
    
    def get_selection_extents(self) -> NavlibBox : ...
    
    def get_selection_transform(self) -> NavlibMatrix : ...
    
    def get_is_selection_empty(self) -> bool : ...
    
    def get_pivot_visible(self) -> bool : ...
    
    def get_camera_matrix(self) -> NavlibMatrix : ...
    
    def get_model_extents(self) -> NavlibBox : ...
    
    def get_pivot_position(self) -> NavlibVector : ...
    
    def get_hit_look_at(self) -> NavlibVector : ...
    
    def is_user_pivot(self) -> bool : ...
    
    def get_coordinate_system(self) -> NavlibMatrix : ...
    
    def get_front_view(self) -> NavlibMatrix : ...
    
    def get_units_to_meters(self) -> float : ...
    
    def get_floor_plane(self) -> NavlibPlane : ...

    def get_camera_target(self) -> NavlibVector : ...
    
    def get_view_construction_plane(self) -> NavlibPlane : ...
    
    def get_is_view_rotatable(self) -> bool : ...
    
    def get_view_focus_distance(self) -> float : ...



    def set_camera_matrix(self, matrix : NavlibMatrix) : ...
    
    def set_view_extents(self, extents : NavlibBox) : ...
    
    def set_view_fov(self, fov : float) : ...
    
    def set_view_frustum(self, frustum : NavlibFrustum) : ...
    
    def set_selection_transform(self, matrix : NavlibMatrix) : ...
    
    def set_pivot_position(self, position : NavlibVector) : ...
    
    def set_pivot_visible(self, visible : bool) : ...
    
    def set_hit_aperture(self, aperture : float) : ...
    
    def set_hit_direction(self, direction : NavlibVector) : ...
    
    def set_hit_look_from(self, eye : NavlibVector) : ...

    def set_hit_selection_only(self, onlySelection : bool) : ...
    
    def set_active_command(self, commandId : str) : ...
        
    def set_motion_flag(self, flag : bool) : ...
    
    def set_settings_changed(self, count : int) : ...
    
    def set_key_press(self, vkey : int) : ...
    
    def set_key_release(self, vkey : int) : ...
    
    def set_transaction(self, transaction : int) : ...
    
    def set_camera_target(self, target : NavlibVector) : ...
    
    def set_pointer_position(self, position : NavlibVector) : ...

    # Private

    def _get_pointer_position(self) :
        try:
            pointer_position = self.get_pointer_position()
            if not isinstance(pointer_position, NavlibVector):
                if self._verbose_mode: logging.warning('get_pointer_position: no valid data provided')
            else:
                return pynavlib.NavlibPoint(pointer_position._x, pointer_position._y, pointer_position._z)
        except Exception as exc:
            logging.exception(f'get_pointer_position exception: {type(exc)}')

    def _get_view_extents(self) : 
        try:
            view_volume = self.get_view_extents()
            if not isinstance(view_volume, NavlibBox):
                if self._verbose_mode: logging.warning('get_view_extents: no valid data provided')
            else:
                return pynavlib.NavlibBox(view_volume._min._x, view_volume._min._y, view_volume._min._z, 
                                          view_volume._max._x, view_volume._max._y, view_volume._max._z)
        except Exception as exc:
            logging.exception(f'get_view_extents exception: {type(exc)}')
    
    def _get_view_fov(self) :
        try:
            view_fov = self.get_view_fov()
            if not isinstance(view_fov, float):
                if self._verbose_mode: logging.warning('get_view_fov: no valid data provided')
            else:
                return view_fov
        except Exception as exc:
            logging.exception(f'get_view_fov exception: {type(exc)}')
    
    def _get_view_frustum(self) :
        try:
            view_frustum = self.get_view_frustum()
            if not isinstance(view_frustum, NavlibFrustum):
                if self._verbose_mode: logging.warning('get_view_frustum: no valid data provided')
            else:
                return pynavlib.NavlibFrustum(view_frustum._left, view_frustum._right,
                                              view_frustum._bottom, view_frustum._top,
                                              view_frustum._near, view_frustum._far)
        except Exception as exc:
            logging.exception(f'get_view_frustum exception: {type(exc)}')
    
    def _get_is_view_perspective(self) :
        try:
            is_view_perspective = self.get_is_view_perspective()
            if not isinstance(is_view_perspective, bool):
                if self._verbose_mode: logging.warning('get_is_view_perspective: no valid data provided')
            else:
                return is_view_perspective
        except Exception as exc:
            logging.exception(f'get_is_view_perspective exception: {type(exc)}')
    
    def _get_selection_extents(self) :
        try:
            selection_extents = self.get_selection_extents()
            if not isinstance(selection_extents, NavlibBox):
                if self._verbose_mode: logging.warning('get_selection_extents: no valid data provided')
            else:
                return pynavlib.NavlibBox(selection_extents._min._x, selection_extents._min._y, selection_extents._min._z, 
                                          selection_extents._max._x, selection_extents._max._y, selection_extents._max._z)
        except Exception as exc:
            logging.exception(f'get_selection_extents exception: {type(exc)}')
    
    def _get_selection_transform(self) :
        try:
            nl_matrix = self.get_selection_transform()
            if not isinstance(nl_matrix, NavlibMatrix):
                if self._verbose_mode: logging.warning('get_selection_transform: no valid data provided')
            else:
                matrix = nl_matrix._matrix
                return pynavlib.NavlibMatrix(matrix[0][0], matrix[0][1], matrix[0][2], matrix[0][3],
                                             matrix[1][0], matrix[1][1], matrix[1][2], matrix[1][3],
                                             matrix[2][0], matrix[2][1], matrix[2][2], matrix[2][3],
                                             matrix[3][0], matrix[3][1], matrix[3][2], matrix[3][3])
        except Exception as exc:
            logging.exception(f'get_selection_transform exception: {type(exc)}')
    
    def _get_is_selection_empty(self) : 
        try:
            is_selection_empty = self.get_is_selection_empty()
            if not isinstance(is_selection_empty, bool):
                if self._verbose_mode: logging.warning('get_is_selection_empty: no valid data provided')
            else:
                return is_selection_empty
        except Exception as exc:
            logging.exception(f'get_is_selection_empty exception: {type(exc)}')
    
    def _get_pivot_visible(self) : 
        try:
            is_pivot_visible = self.get_pivot_visible()
            if not isinstance(is_pivot_visible, bool):
                if self._verbose_mode: logging.warning('get_pivot_visible: no valid data provided')
            else:
                return is_pivot_visible
        except Exception as exc:
            logging.exception(f'get_pivot_visible exception: {type(exc)}')
    
    def _get_camera_matrix(self) : 
        try:
            nl_matrix = self.get_camera_matrix()
            if not isinstance(nl_matrix, NavlibMatrix):
                if self._verbose_mode: logging.warning('get_camera_matrix: no valid data provided')
            else:
                matrix = nl_matrix._matrix
                return pynavlib.NavlibMatrix(matrix[0][0], matrix[0][1], matrix[0][2], matrix[0][3],
                                             matrix[1][0], matrix[1][1], matrix[1][2], matrix[1][3],
                                             matrix[2][0], matrix[2][1], matrix[2][2], matrix[2][3],
                                             matrix[3][0], matrix[3][1], matrix[3][2], matrix[3][3])
        except Exception as exc:
            logging.exception(f'get_camera_matrix exception: {type(exc)}')
    
    def _get_model_extents(self) : 
        try:
            model_extents = self.get_model_extents()
            if not isinstance(model_extents, NavlibBox):
                if self._verbose_mode: logging.warning('get_model_extents: no valid data provided')
            else:
                return pynavlib.NavlibBox(model_extents._min._x, model_extents._min._y, model_extents._min._z, 
                                          model_extents._max._x, model_extents._max._y, model_extents._max._z)
        except Exception as exc:
            logging.exception(f'get_model_extents exception: {type(exc)}')

    def _get_pivot_position(self) :
        try:
            pivot_position = self.get_pivot_position()
            if not isinstance(pivot_position, NavlibVector):
                if self._verbose_mode: logging.warning('get_pivot_position: no valid data provided')
            else:
                return pynavlib.NavlibPoint(pivot_position._x, pivot_position._y, pivot_position._z)
        except Exception as exc:
            logging.exception(f'get_pivot_position exception: {type(exc)}')
    
    def _get_hit_look_at(self) :
        try:
            hit_position = self.get_hit_look_at()
            if not isinstance(hit_position, NavlibVector):
                if self._verbose_mode: logging.warning('get_hit_look_at: no valid data provided')
            else:
                return pynavlib.NavlibPoint(hit_position._x, hit_position._y, hit_position._z)
        except Exception as exc:
            logging.exception(f'get_hit_look_at exception: {type(exc)}')

    def _is_user_pivot(self) :
        try:
            is_user_pivot = self.is_user_pivot()
            if not isinstance(is_user_pivot, bool):
                if self._verbose_mode: logging.warning('is_user_pivot: no valid data provided')
            else:
                return is_user_pivot
        except Exception as exc:
            logging.exception(f'is_user_pivot exception: {type(exc)}')
    
    def _get_coordinate_system(self) :
        try:
            nl_matrix = self.get_coordinate_system()
            if not isinstance(nl_matrix, NavlibMatrix):
                if self._verbose_mode: logging.warning('get_coordinate_system: no valid data provided')
            else:
                matrix = nl_matrix._matrix
                return pynavlib.NavlibMatrix(matrix[0][0], matrix[0][1], matrix[0][2], matrix[0][3],
                                             matrix[1][0], matrix[1][1], matrix[1][2], matrix[1][3],
                                             matrix[2][0], matrix[2][1], matrix[2][2], matrix[2][3],
                                             matrix[3][0], matrix[3][1], matrix[3][2], matrix[3][3])
        except Exception as exc:
            logging.exception(f'get_coordinate_system exception: {type(exc)}')

    def _get_front_view(self) :
        try:
            nl_matrix = self.get_front_view()
            if not isinstance(nl_matrix, NavlibMatrix):
                if self._verbose_mode: logging.warning('get_front_view: no valid data provided')
            else:
                matrix = nl_matrix._matrix
                return pynavlib.NavlibMatrix(matrix[0][0], matrix[0][1], matrix[0][2], matrix[0][3],
                                             matrix[1][0], matrix[1][1], matrix[1][2], matrix[1][3],
                                             matrix[2][0], matrix[2][1], matrix[2][2], matrix[2][3],
                                             matrix[3][0], matrix[3][1], matrix[3][2], matrix[3][3])
        except Exception as exc:
            logging.exception(f'get_front_view exception: {type(exc)}')

    def _get_units_to_meters(self) :
        try:
            units_to_meters = self.get_units_to_meters()
            if not isinstance(units_to_meters, float):
                if self._verbose_mode: logging.warning('get_units_to_meters: no valid data provided')
            else:
                return units_to_meters
        except Exception as exc:
            logging.exception(f'get_units_to_meters exception: {type(exc)}')
    
    def _get_floor_plane(self) :
        try:
            floor_plane = self.get_floor_plane()
            if not isinstance(floor_plane, NavlibPlane):
                if self._verbose_mode: logging.warning('get_floor_plane: no valid data provided')
            else:
                return pynavlib.NavlibPlane(floor_plane._normal._x, floor_plane._normal._y, floor_plane._normal._z, floor_plane._distance)
        except Exception as exc:
            logging.exception(f'get_floor_plane exception: {type(exc)}')

    def _get_camera_target(self) :
        try:
            camera_target = self.get_camera_target()
            if not isinstance(camera_target, NavlibVector):
                if self._verbose_mode: logging.warning('get_camera_target: no valid data provided')
            else:
                return pynavlib.NavlibPoint(camera_target._x, camera_target._y, camera_target._z)
        except Exception as exc:
            logging.exception(f'get_camera_target exception: {type(exc)}')

    def _get_view_construction_plane(self) :
        try:
            construction_plane = self.get_view_construction_plane()
            if not isinstance(construction_plane, NavlibPlane):
                if self._verbose_mode: logging.warning('get_view_construction_plane: no valid data provided')
            else:
                return pynavlib.NavlibPlane(construction_plane._normal._x, construction_plane._normal._y, construction_plane._normal._z, construction_plane._distance)
        except Exception as exc:
            logging.exception(f'get_view_construction_plane exception: {type(exc)}')

    def _get_is_view_rotatable(self) :
        try:
            is_view_rotatable = self.get_is_view_rotatable()
            if not isinstance(is_view_rotatable, bool):
                if self._verbose_mode: logging.warning('get_is_view_rotatable: no valid data provided')
            else:
                return is_view_rotatable
        except Exception as exc:
            logging.exception(f'get_is_view_rotatable exception: {type(exc)}')
    
    def _get_view_focus_distance(self) :
        try:
            view_focus_distance = self.get_view_focus_distance()
            if not isinstance(view_focus_distance, float):
                if self._verbose_mode: logging.warning('get_view_focus_distance: no valid data provided')
            else:
                return view_focus_distance
        except Exception as exc:
            logging.exception(f'get_view_focus_distance exception: {type(exc)}')
     

    def _set_camera_matrix(self, matrix) : 
        self.set_camera_matrix(NavlibMatrix([[matrix.m00, matrix.m01, matrix.m02, matrix.m03],
                                              [matrix.m10, matrix.m11, matrix.m12, matrix.m13],
                                              [matrix.m20, matrix.m21, matrix.m22, matrix.m23],
                                              [matrix.m30, matrix.m31, matrix.m32, matrix.m33]]))
    
    def _set_view_extents(self, extents) :
        self.set_view_extents(NavlibBox(NavlibVector(extents.min.x, extents.min.y, extents.min.z),
                                        NavlibVector(extents.max.x, extents.max.y, extents.max.z)))
    
    def _set_view_fov(self, fov) :
        self.set_view_fov(fov)
    
    def _set_view_frustum(self, frustum) :
        self.set_view_frustum(NavlibFrustum(frustum.left, frustum.right,
                                             frustum.bottom, frustum.top,
                                             frustum.near_plane, frustum.far_plane))
    
    def _set_selection_transform(self, matrix) :
        self.set_selection_transform(NavlibMatrix([[matrix.m00, matrix.m01, matrix.m02, matrix.m03],
                                                    [matrix.m10, matrix.m11, matrix.m12, matrix.m13],
                                                    [matrix.m20, matrix.m21, matrix.m22, matrix.m23],
                                                    [matrix.m30, matrix.m31, matrix.m32, matrix.m33]]))
    
    def _set_pivot_position(self, position) :
        self.set_pivot_position(NavlibVector(position.x, position.y, position.z))
    
    def _set_pivot_visible(self, visible) :
        self.set_pivot_visible(visible)
    
    def _set_hit_aperture(self, aperture) :
        self.set_hit_aperture(aperture)
    
    def _set_hit_direction(self, direction) :
        self.set_hit_direction(NavlibVector(direction.x, direction.y, direction.z))
    
    def _set_hit_look_from(self, eye) :
        self.set_hit_look_from(NavlibVector(eye.x, eye.y, eye.z))

    def _set_hit_selection_only(self, onlySelection) :
        self.set_hit_selection_only(onlySelection)
    
    def _set_active_command(self, commandId) :
        self.set_active_command(commandId)

    def _set_motion_flag(self, flag) :
        self.set_motion_flag(flag)
    
    def _set_settings_changed(self, count) :
        self.set_settings_changed(count)
    
    def _set_key_press(self, vkey) :
        self.set_key_press(vkey)
    
    def _set_key_release(self, vkey) :
        self.set_key_release(vkey)
    
    def _set_transaction(self, transaction) :
        self.set_transaction(transaction)
    
    def _set_camera_target(self, target) :
        self.set_camera_target(NavlibVector(target.x, target.y, target.z))
    
    def _set_pointer_position(self, position) :
        self.set_pointer_position(NavlibVector(position.x, position.y, position.z))