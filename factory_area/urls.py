# factory_area/urls.py
from django.urls import path
from . import views

app_name = 'factory_area'

urlpatterns = [
    # 首页
    path('', views.home, name='home'),

    # 厂区相关...
    path('areas/', views.factory_area_list, name='list'),
    path('areas/add/', views.factory_area_add, name='add'),
    path('areas/<int:pk>/edit/', views.factory_area_edit, name='edit'),
    path('areas/<int:pk>/disable/', views.factory_area_disable, name='disable'),  # 重命名
    path('areas/<int:pk>/enable/', views.factory_area_enable, name='enable'),    # 新增
#    path('areas/<int:pk>/toggle/', views.factory_area_toggle, name='toggle'),    # 新增：切换状态

    # 楼层相关
    path('floors/', views.floor_list, name='floor_list'),
    path('floors/add/', views.floor_add, name='floor_add'),
    path('floors/<int:pk>/edit/', views.floor_edit, name='floor_edit'),
    path('floors/<int:pk>/disable/', views.floor_disable, name='floor_disable'),
    path('floors/<int:pk>/enable/', views.floor_enable, name='floor_enable'),

    # 线体相关
    path('lines/', views.line_list, name='line_list'),
    path('lines/add/', views.line_add, name='line_add'),
    path('lines/<int:pk>/edit/', views.line_edit, name='line_edit'),
    path('lines/<int:pk>/disable/', views.line_disable, name='line_disable'),
    path('lines/<int:pk>/enable/', views.line_enable, name='line_enable'),

    # 设备类型相关
    path('equipment-types/', views.equipment_type_list, name='equipment_type_list'),
    path('equipment-types/add/', views.equipment_type_add, name='equipment_type_add'),
    path('equipment-types/<int:pk>/edit/', views.equipment_type_edit, name='equipment_type_edit'),
    path('equipment-types/<int:pk>/disable/', views.equipment_type_disable, name='equipment_type_disable'),
    path('equipment-types/<int:pk>/enable/', views.equipment_type_enable, name='equipment_type_enable'),

        # 设备实例相关
    path('devices/', views.device_list, name='device_list'),
    path('devices/add/', views.device_add, name='device_add'),
    path('devices/<int:pk>/edit/', views.device_edit, name='device_edit'),
    path('devices/<int:pk>/disable/', views.device_disable, name='device_disable'),
    path('devices/<int:pk>/enable/', views.device_enable, name='device_enable'),
    path('devices/<int:pk>/detail/', views.device_detail, name='device_detail'),

    # 设备纳管配置相关
    path('maintenance-profiles/', views.maintenance_profile_list, name='maintenance_profile_list'),
    path('maintenance-profiles/batch-create/', views.maintenance_profile_batch_create, name='maintenance_profile_batch_create'),
    path('maintenance-profiles/batch-reset/', views.maintenance_profile_batch_reset, name='maintenance_profile_batch_reset'),
    path('maintenance-profiles/<int:device_id>/edit/', views.maintenance_profile_edit, name='maintenance_profile_edit'),

]