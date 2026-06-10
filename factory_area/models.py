from django.db import models

class FactoryArea(models.Model):
    """厂区表 - 对应文档中的Site"""
    factory_area_code = models.CharField(max_length=50, unique=True, verbose_name="厂区编码")
    name = models.CharField(max_length=100, verbose_name="厂区名称")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = 'factory_area'  # 强制表名为factory_area（而不是factory_area_factoryarea）
        verbose_name = "厂区"
        verbose_name_plural = "厂区管理"
    
    def __str__(self):
        return f"{self.factory_area_code} - {self.name}"


class Floor(models.Model):
    """楼层表"""
    floor_code = models.CharField(max_length=50, unique=True, verbose_name="楼层编码")
    name = models.CharField(max_length=100, verbose_name="楼层名称")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        db_table = 'floor'  # 强制表名为floor
        verbose_name = "楼层"
        verbose_name_plural = "楼层管理"
    
    def __str__(self):
        return self.name


class Line(models.Model):
    """线体表"""
    line_name = models.CharField(max_length=100, unique=True, verbose_name="线体名称")
    factory_area = models.ForeignKey(
        FactoryArea, 
        on_delete=models.CASCADE, 
        verbose_name="所属厂区"
    )
    floor = models.ForeignKey(
        Floor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="所在楼层"
    )
    owner_person_id = models.CharField(max_length=50, verbose_name="责任人ID")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = 'line'  # 强制表名为line
        verbose_name = "线体"
        verbose_name_plural = "线体管理"
        # 同一厂区内线体编码唯一
        #unique_together = ['factory_area', 'line_code']
        ordering = ['line_name']

    
    def __str__(self):
        return self.line_name
    

class EquipmentType(models.Model):
    """设备类型（包含校验器具类型）"""
    # 基本属性
    equipment_type_id = models.CharField(max_length=50, unique=True, verbose_name="类型ID")
    name = models.CharField(max_length=100, verbose_name="类型名称")
    
    # 设备类别选择
    DEVICE_CATEGORY_CHOICES = [
        ('self_made', '自制设备'),
        ('purchased', '客供设备'),
        ('calibration_tool', '市购设备'),
    ]
    device_category = models.CharField(
        max_length=20,
        choices=DEVICE_CATEGORY_CHOICES,
        verbose_name="设备类别"
    )
    
    # 厂商信息
    brand = models.CharField(max_length=100, blank=True, verbose_name="品牌/厂商")
    model = models.CharField(max_length=100, blank=True, verbose_name="型号")
    
    # 送校方式选择
    CALIBRATION_METHOD_CHOICES = [
        ('internal', '内部校准'),
        ('external', '外部送检'),
        ('hybrid', '内外结合'),
        ('none', '无需校准'),
    ]
    calibration_method = models.CharField(
        max_length=20,
        choices=CALIBRATION_METHOD_CHOICES,
        default='none',
        verbose_name="送校方式"
    )
    
    # 默认维保/校正规则
    maintenance_required = models.BooleanField(default=True, verbose_name="需要保养")
    calibration_required = models.BooleanField(default=False, verbose_name="需要校正")
    maintenance_interval_days = models.IntegerField(default=180, verbose_name="保养周期(天)")
    calibration_interval_days = models.IntegerField(default=365, verbose_name="校正周期(天)")
    maintenance_duration_min = models.IntegerField(default=60, verbose_name="保养预计工时(分钟)")
    calibration_duration_min = models.IntegerField(default=120, verbose_name="校正预计工时(分钟)")
    
    # 成本估算
    estimated_unit_cost = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="预估单价"
    )
    currency = models.CharField(max_length=10, default='CNY', verbose_name="币种")
    cost_source = models.CharField(max_length=100, blank=True, verbose_name="成本来源")
    cost_updated_at = models.DateField(null=True, blank=True, verbose_name="成本更新时间")
    
    # 主数据控制
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = 'equipment_type'
        verbose_name = "设备类型"
        verbose_name_plural = "设备类型管理"
        ordering = ['equipment_type_id']
    
    def __str__(self):
        return f"{self.equipment_type_id} - {self.name}"
    
    def get_category_display_name(self):
        return dict(self.DEVICE_CATEGORY_CHOICES).get(self.device_category, self.device_category)
    
    def get_calibration_method_display_name(self):
        return dict(self.CALIBRATION_METHOD_CHOICES).get(self.calibration_method, self.calibration_method)
    
    @property
    def total_estimated_cost(self):
        """计算总预估成本（如果有单价）"""
        if self.estimated_unit_cost:
            # 这里可以扩展为乘以数量等
            return self.estimated_unit_cost
        return 0


class AttachmentType(models.Model):
    """附件类别"""
    ATTACHMENT_TYPE_CHOICES = [
        ('calibration_sop', '校验SOP'),
        ('calibration_tool_list', '校验器具/工具清单'),
        ('manual', '说明书'),
        ('quote', '报价单'),
        ('certificate', '证书'),
        ('other', '其他'),
    ]
    
    attachment_type = models.CharField(
        max_length=30,
        choices=ATTACHMENT_TYPE_CHOICES,
        unique=True,
        verbose_name="附件类别"
    )
    description = models.TextField(blank=True, verbose_name="描述")
    is_required = models.BooleanField(default=True, verbose_name="是否必填")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    
    class Meta:
        db_table = 'attachment_type'
        verbose_name = "附件类别"
        verbose_name_plural = "附件类别管理"
    
    def __str__(self):
        return self.get_attachment_type_display()


class EquipmentTypeAttachmentRequirement(models.Model):
    """设备类型与附件要求的关联表"""
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.CASCADE,
        related_name='attachment_requirements',
        verbose_name="设备类型"
    )
    attachment_type = models.ForeignKey(
        AttachmentType,
        on_delete=models.CASCADE,
        verbose_name="附件类别"
    )
    is_required = models.BooleanField(default=True, verbose_name="是否必填")
    notes = models.TextField(blank=True, verbose_name="备注")
    
    class Meta:
        db_table = 'equipment_type_attachment_requirement'
        verbose_name = "设备类型附件要求"
        verbose_name_plural = "设备类型附件要求"
        unique_together = ['equipment_type', 'attachment_type']
    
    def __str__(self):
        return f"{self.equipment_type} - {self.attachment_type}"


class EquipmentTypeToolRequirement(models.Model):
    """设备类型需要的校验器具类型及数量"""
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.CASCADE,
        related_name='tool_requirements',
        verbose_name="设备类型"
    )
    required_tool_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.CASCADE,
        related_name='required_by_equipment_types',
        verbose_name="所需校验器具类型",
        limit_choices_to={'device_category': 'calibration_tool'}  # 只能选择校验器具类型的设备类型
    )
    required_quantity = models.IntegerField(default=1, verbose_name="需要数量")
    notes = models.TextField(blank=True, verbose_name="备注")
    
    class Meta:
        db_table = 'equipment_type_tool_requirement'
        verbose_name = "设备类型工具要求"
        verbose_name_plural = "设备类型工具要求"
        unique_together = ['equipment_type', 'required_tool_type']
    
    def __str__(self):
        return f"{self.equipment_type} 需要 {self.required_quantity} 个 {self.required_tool_type}"
    
    @property
    def estimated_tool_cost(self):
        """计算所需校验器具的预估成本"""
        if self.required_tool_type.estimated_unit_cost:
            return self.required_tool_type.estimated_unit_cost * self.required_quantity
        return 0
    

class Device(models.Model):
    """设备实例台账"""
    # 设备基本信息
    device_id = models.AutoField(primary_key=True, verbose_name="设备ID")
    ppid = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="PPID",
        help_text="每台设备的唯一标识，必填"
    )
    asset_tag = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="固定资产编号",
        help_text="若有固定资产编号则填写"
    )
    device_code = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="设备编码",
        help_text="现场编号/铭牌编号/内部编号"
    )
    device_name = models.CharField(
        max_length=200, 
        blank=True, 
        verbose_name="设备名称",
        help_text="如不填写，将自动生成：类型名称+PPID"
    )
    
    # 关联信息
    equipment_type = models.ForeignKey(
        EquipmentType,
        on_delete=models.PROTECT,
        verbose_name="设备类型",
        help_text="必须选择一个设备类型",
        related_name='devices'
    )
    
    # 责任人/归属信息
    department_name = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="归属部门/团队"
    )
    keeper = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="保管责任人",
        help_text="保管人/责任人ID"
    )
    
    # RFID信息
    rfid_tag = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        unique=True,
        verbose_name="RFID标签",
        help_text="有值则必须唯一"
    )
    inventory_external_id = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="盘点系统ID"
    )
    rfid_enrolled_at = models.DateTimeField(
        blank=True, 
        null=True,
        verbose_name="RFID纳入时间"
    )
    
    # 运行状态
    OPERATIONAL_STATE_CHOICES = [
        ('IN_USE', '使用中'),
        ('SPARE', '备品/备用'),
        ('IDLE', '闲置可用'),
        ('WAITING_FOR_REPAIR', '待维修'),
        ('IN_MAINTENANCE', '维修/保养/校正中'),
        ('QUARANTINED', '隔离/冻结'),
        ('PENDING_DISPOSAL', '待报废/待处置'),
        ('OUT_OF_SERVICE', '已报废/不可用'),
    ]
    operational_state = models.CharField(
        max_length=20,
        choices=OPERATIONAL_STATE_CHOICES,
        default='IDLE',
        verbose_name="运行状态"
    )
    
    # 位置信息
    LOCATION_TYPE_CHOICES = [
        ('LINE', '线体'),
        ('WAREHOUSE', '仓库'),
        ('LAB', '实验室'),
        ('OTHER', '其他'),
    ]
    location_type = models.CharField(
        max_length=20,
        choices=LOCATION_TYPE_CHOICES,
        default='OTHER',
        verbose_name="位置类型"
    )
    line = models.ForeignKey(
        Line,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="所在线体",
        help_text="当位置类型为'线体'时填写"
    )
    location_text = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name="位置描述",
        help_text="非线体位置，如仓库/维修间/库位"
    )
    area = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="区域/工位",
        help_text="线上设备：例CC10、CC11等；非线上设备：例仓库、维修间等"
    )
    
    # 主数据控制
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        db_table = 'device'
        verbose_name = "设备实例"
        verbose_name_plural = "设备实例管理"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.ppid} - {self.get_device_display_name()}"
    
    def get_device_display_name(self):
        """获取设备显示名称"""
        if self.device_name:
            return self.device_name
        elif self.equipment_type:
            return f"{self.equipment_type.name} - {self.ppid}"
        else:
            return self.ppid
    
    def save(self, *args, **kwargs):
        # 如果设备名称为空，自动生成
        if not self.device_name and self.equipment_type:
            self.device_name = f"{self.equipment_type.name} - {self.ppid}"
        
        # 校验设备类型是否启用
        if not self.equipment_type.is_active and self.is_active:
            raise ValueError("不能使用已禁用的设备类型创建启用状态的设备")
        
        super().save(*args, **kwargs)
    
    @property
    def can_be_transferred(self):
        """判断设备是否可调拨"""
        non_transferable_states = [
            'IN_MAINTENANCE', 
            'WAITING_FOR_REPAIR', 
            'QUARANTINED', 
            'PENDING_DISPOSAL', 
            'OUT_OF_SERVICE'
        ]
        return self.operational_state not in non_transferable_states
    
    @property
    def is_idle_or_spare(self):
        """判断设备是否为闲置或备品"""
        return self.operational_state in ['IDLE', 'SPARE']
    
    def get_operational_state_display_name(self):
        return dict(self.OPERATIONAL_STATE_CHOICES).get(self.operational_state, self.operational_state)

    def get_location_type_display_name(self):
        return dict(self.LOCATION_TYPE_CHOICES).get(self.location_type, self.location_type)


class DeviceMaintenanceProfile(models.Model):
    """设备纳管配置表 - 1:1绑定设备实例"""
    device = models.OneToOneField(
        Device,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='maintenance_profile',
        verbose_name="设备实例"
    )

    # 纳管开关（总开关）
    enable_maintenance = models.BooleanField(default=True, verbose_name="是否纳入维保体系")

    # 继承/覆盖选择
    use_type_defaults = models.BooleanField(default=True, verbose_name="使用类型默认值")

    # 单台覆盖字段（仅当 use_type_defaults=false 才生效）
    maintenance_required = models.BooleanField(default=True, verbose_name="是否需要保养（覆盖）")
    calibration_required = models.BooleanField(default=False, verbose_name="是否需要校正（覆盖）")
    maintenance_interval_days = models.IntegerField(default=180, verbose_name="保养周期(天,覆盖)")
    calibration_interval_days = models.IntegerField(default=365, verbose_name="校正周期(天,覆盖)")
    maintenance_duration_min = models.IntegerField(default=60, verbose_name="保养预计工时(分钟,覆盖)")
    calibration_duration_min = models.IntegerField(default=120, verbose_name="校正预计工时(分钟,覆盖)")

    # 追溯字段
    effective_from = models.DateTimeField(auto_now_add=True, verbose_name="规则生效时间")
    last_updated_by = models.CharField(max_length=50, blank=True, verbose_name="更新人")
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    status = models.BooleanField(default=True, verbose_name="启用状态")

    class Meta:
        db_table = 'device_maintenance_profile'
        verbose_name = "设备纳管配置"
        verbose_name_plural = "设备纳管配置管理"

    def __str__(self):
        return f"{self.device.ppid} - 纳管配置"

    @property
    def is_active(self):
        return self.status

    @property
    def get_maintenance_required(self):
        """获取是否需要保养（考虑继承）"""
        if self.use_type_defaults and self.device.equipment_type:
            return self.device.equipment_type.maintenance_required
        return self.maintenance_required

    @property
    def get_calibration_required(self):
        """获取是否需要校正（考虑继承）"""
        if self.use_type_defaults and self.device.equipment_type:
            return self.device.equipment_type.calibration_required
        return self.calibration_required

    @property
    def get_maintenance_interval(self):
        """获取保养周期（考虑继承）"""
        if self.use_type_defaults and self.device.equipment_type:
            return self.device.equipment_type.maintenance_interval_days
        return self.maintenance_interval_days

    @property
    def get_calibration_interval(self):
        """获取校正周期（考虑继承）"""
        if self.use_type_defaults and self.device.equipment_type:
            return self.device.equipment_type.calibration_interval_days
        return self.calibration_interval_days

    @property
    def get_maintenance_duration(self):
        """获取保养工时（考虑继承）"""
        if self.use_type_defaults and self.device.equipment_type:
            return self.device.equipment_type.maintenance_duration_min
        return self.maintenance_duration_min

    @property
    def get_calibration_duration(self):
        """获取校正工时（考虑继承）"""
        if self.use_type_defaults and self.device.equipment_type:
            return self.device.equipment_type.calibration_duration_min
        return self.calibration_duration_min

    def save(self, *args, **kwargs):
        # 自动初始化：如果是新创建的profile，设置默认值
        if self._state.adding and self.device.equipment_type:
            equipment_type = self.device.equipment_type
            if self.use_type_defaults:
                # 使用类型默认值
                self.maintenance_required = equipment_type.maintenance_required
                self.calibration_required = equipment_type.calibration_required
                self.maintenance_interval_days = equipment_type.maintenance_interval_days
                self.calibration_interval_days = equipment_type.calibration_interval_days
                self.maintenance_duration_min = equipment_type.maintenance_duration_min
                self.calibration_duration_min = equipment_type.calibration_duration_min

            # 默认纳管状态根据设备类型决定
            self.enable_maintenance = equipment_type.maintenance_required or equipment_type.calibration_required

        super().save(*args, **kwargs)