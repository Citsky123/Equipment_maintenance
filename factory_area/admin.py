# factory_area/admin.py
from django.contrib import admin
from .models import (
    FactoryArea, Floor, Line,
    EquipmentType, AttachmentType,
    EquipmentTypeAttachmentRequirement, EquipmentTypeToolRequirement,
    Device, DeviceMaintenanceProfile
)

@admin.register(FactoryArea)
class FactoryAreaAdmin(admin.ModelAdmin):
    list_display = ['factory_area_code', 'name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['factory_area_code', 'name']
    list_editable = ['is_active']

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ['floor_code', 'name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['floor_code', 'name']
    list_editable = ['is_active']

@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = ['line_name', 'factory_area', 'floor', 'owner_person_id', 'is_active']
    list_filter = ['is_active', 'factory_area']
    search_fields = ['line_name', 'owner_person_id']
    list_editable = ['is_active']

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = [
        'equipment_type_id', 'name', 'device_category', 'brand', 
        'model', 'calibration_method', 'is_active'
    ]
    list_filter = ['device_category', 'calibration_method', 'is_active']
    search_fields = ['equipment_type_id', 'name', 'brand', 'model']  # 添加搜索字段
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(AttachmentType)
class AttachmentTypeAdmin(admin.ModelAdmin):
    list_display = ['attachment_type', 'description', 'is_required', 'is_active']
    list_filter = ['is_required', 'is_active']
    list_editable = ['is_active']
    # 添加以下搜索字段
    search_fields = ['attachment_type', 'description']

@admin.register(EquipmentTypeAttachmentRequirement)
class EquipmentTypeAttachmentRequirementAdmin(admin.ModelAdmin):
    list_display = ['equipment_type', 'attachment_type', 'is_required']
    list_filter = ['is_required']
    # 确保引用的模型有search_fields
    autocomplete_fields = ['equipment_type', 'attachment_type']

@admin.register(EquipmentTypeToolRequirement)
class EquipmentTypeToolRequirementAdmin(admin.ModelAdmin):
    list_display = ['equipment_type', 'required_tool_type', 'required_quantity']
    list_filter = ['equipment_type__device_category']
    # 确保引用的模型有search_fields
    autocomplete_fields = ['equipment_type', 'required_tool_type']

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'ppid', 'device_name', 'equipment_type', 'operational_state',
        'department_name', 'keeper', 'is_active'
    ]
    list_filter = [
        'is_active', 'operational_state', 'equipment_type__device_category',
        'location_type'
    ]
    search_fields = [
        'ppid', 'device_name', 'device_code', 'asset_tag', 
        'rfid_tag', 'department_name', 'keeper'
    ]
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['equipment_type', 'line']
    fieldsets = (
        ('基本信息', {
            'fields': ('ppid', 'device_name', 'device_code', 'asset_tag')
        }),
        ('关联信息', {
            'fields': ('equipment_type', 'department_name', 'keeper')
        }),
        ('RFID信息', {
            'fields': ('rfid_tag', 'inventory_external_id', 'rfid_enrolled_at')
        }),
        ('运行状态与位置', {
            'fields': ('operational_state', 'location_type', 'line', 'location_text', 'area')
        }),
        ('系统信息', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(DeviceMaintenanceProfile)
class DeviceMaintenanceProfileAdmin(admin.ModelAdmin):
    list_display = [
        'device', 'enable_maintenance', 'use_type_defaults',
        'get_maintenance_required_display',
        'get_calibration_required_display',
        'get_maintenance_interval_display',
        'get_calibration_interval_display',
        'status', 'last_updated_at'
    ]
    list_filter = [
        'enable_maintenance', 'use_type_defaults', 'status',
        'device__operational_state',
        'device__equipment_type__device_category'
    ]
    search_fields = [
        'device__ppid', 'device__device_name', 'device__device_code',
        'last_updated_by'
    ]
    list_editable = ['enable_maintenance', 'use_type_defaults', 'status']
    readonly_fields = ['effective_from', 'last_updated_at']
    autocomplete_fields = ['device']

    fieldsets = (
        ('设备信息', {
            'fields': ('device',)
        }),
        ('纳管开关', {
            'fields': ('enable_maintenance', 'use_type_defaults', 'status')
        }),
        ('单台覆盖配置（仅当不使用类型默认值时生效）', {
            'fields': (
                'maintenance_required', 'calibration_required',
                'maintenance_interval_days', 'calibration_interval_days',
                'maintenance_duration_min', 'calibration_duration_min'
            ),
            'classes': ('collapse',)
        }),
        ('追溯信息', {
            'fields': ('effective_from', 'last_updated_by', 'last_updated_at')
        }),
    )

    def get_maintenance_required_display(self, obj):
        """显示实际生效的保养需求状态"""
        if obj:
            return "是" if obj.get_maintenance_required else "否"
        return "-"
    get_maintenance_required_display.short_description = "需要保养"

    def get_calibration_required_display(self, obj):
        """显示实际生效的校正需求状态"""
        if obj:
            return "是" if obj.get_calibration_required else "否"
        return "-"
    get_calibration_required_display.short_description = "需要校正"

    def get_maintenance_interval_display(self, obj):
        """显示实际生效的保养周期"""
        if obj:
            return f"{obj.get_maintenance_interval}天"
        return "-"
    get_maintenance_interval_display.short_description = "保养周期"

    def get_calibration_interval_display(self, obj):
        """显示实际生效的校正周期"""
        if obj:
            return f"{obj.get_calibration_interval}天"
        return "-"
    get_calibration_interval_display.short_description = "校正周期"