# factory_area/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import models, transaction
from .models import (
    FactoryArea, Floor, Line, EquipmentType, Device,
    DeviceMaintenanceProfile
)

def home(request):
    """系统首页"""
    # 统计数据
    stats = {
        'factory_areas_count': FactoryArea.objects.count(),
        'floors_count': Floor.objects.count(),
        'lines_count': Line.objects.count(),
        'equipment_types_count': EquipmentType.objects.count(),
        'devices_count': Device.objects.count(),
        'profiles_count': DeviceMaintenanceProfile.objects.count(),
        'enabled_profiles_count': DeviceMaintenanceProfile.objects.filter(enable_maintenance=True).count(),
        'disabled_profiles_count': DeviceMaintenanceProfile.objects.filter(enable_maintenance=False).count(),
    }

    return render(request, 'factory_area/home.html', {'stats': stats})


def factory_area_list(request):
    """厂区列表"""
    # 修改这里：显示所有厂区，不只是激活的
    areas = FactoryArea.objects.all().order_by('-created_at')
    return render(request, 'factory_area/list.html', {'areas': areas})

def factory_area_add(request):
    """新增厂区"""
    if request.method == 'POST':
        code = request.POST.get('factory_area_code')
        name = request.POST.get('name')
        
        # 添加调试信息
        print("="*50)
        print("收到POST请求，准备保存数据")
        print(f"编码: {code}, 名称: {name}")
        print(f"请求方法: {request.method}")
        print(f"POST数据: {dict(request.POST)}")
        
        if FactoryArea.objects.filter(factory_area_code=code).exists():
            print(f"⚠️ 厂区编码 {code} 已存在，拒绝保存")
            messages.error(request, f'厂区编码 {code} 已存在')
        else:
            try:
                # 创建对象
                print(f"正在创建厂区: {code} - {name}")
                area = FactoryArea.objects.create(
                    factory_area_code=code,
                    name=name,
                    is_active=True
                )
                print(f"✅ 保存成功! ID: {area.id}")
                print(f"✅ 创建时间: {area.created_at}")
                
                # 立即查询验证
                verify = FactoryArea.objects.filter(factory_area_code=code).first()
                if verify:
                    print(f"✅ 验证查询成功: {verify.name}")
                else:
                    print("❌ 验证查询失败!")
                
                messages.success(request, f'厂区 {name} 创建成功')
                return redirect('factory_area:list')
                
            except Exception as e:
                print(f"❌ 保存失败，错误信息: {str(e)}")
                import traceback
                traceback.print_exc()
                messages.error(request, f'创建失败: {str(e)}')
    
    return render(request, 'factory_area/form.html')

# factory_area/views.py

def floor_list(request):
    """楼层列表"""
    floors = Floor.objects.all().order_by('floor_code')
    return render(request, 'factory_area/floor_list.html', {'floors': floors})

def floor_add(request):
    """新增楼层"""
    if request.method == 'POST':
        floor_code = request.POST.get('floor_code')
        name = request.POST.get('name')
        
        if Floor.objects.filter(floor_code=floor_code).exists():
            messages.error(request, f'楼层编码 {floor_code} 已存在')
        else:
            Floor.objects.create(
                floor_code=floor_code,
                name=name,
                is_active=True
            )
            messages.success(request, f'楼层 {name} 创建成功')
            return redirect('factory_area:floor_list')
    
    return render(request, 'factory_area/floor_form.html')

def floor_edit(request, pk):
    """编辑楼层"""
    floor = get_object_or_404(Floor, pk=pk)
    
    if request.method == 'POST':
        floor_code = request.POST.get('floor_code')
        name = request.POST.get('name')
        is_active = request.POST.get('is_active') == 'on'
        
        if Floor.objects.filter(floor_code=floor_code).exclude(pk=pk).exists():
            messages.error(request, f'楼层编码 {floor_code} 已存在')
        else:
            floor.floor_code = floor_code
            floor.name = name
            floor.is_active = is_active
            floor.save()
            messages.success(request, f'楼层 {name} 更新成功')
            return redirect('factory_area:floor_list')
    
    return render(request, 'factory_area/floor_form.html', {'floor': floor})

def floor_disable(request, pk):
    """禁用楼层"""
    floor = get_object_or_404(Floor, pk=pk)
    floor.is_active = False
    floor.save()
    messages.success(request, f'楼层 {floor.name} 已禁用')
    return redirect('factory_area:floor_list')

def floor_enable(request, pk):
    """启用楼层"""
    floor = get_object_or_404(Floor, pk=pk)
    floor.is_active = True
    floor.save()
    messages.success(request, f'楼层 {floor.name} 已启用')
    return redirect('factory_area:floor_list')


def factory_area_edit(request, pk):
    """编辑厂区"""
    area = get_object_or_404(FactoryArea, pk=pk)
    
    if request.method == 'POST':
        code = request.POST.get('factory_area_code')
        name = request.POST.get('name')
        is_active = request.POST.get('is_active') == 'on'
        
        # 检查编码是否重复（排除自己）
        if FactoryArea.objects.filter(factory_area_code=code).exclude(pk=pk).exists():
            messages.error(request, f'厂区编码 {code} 已存在')
        else:
            area.factory_area_code = code
            area.name = name
            area.is_active = is_active
            area.save()
            messages.success(request, f'厂区 {name} 更新成功')
            return redirect('factory_area:list')
    
    return render(request, 'factory_area/form.html', {'area': area})

def factory_area_disable(request, pk):
    """禁用厂区"""
    area = get_object_or_404(FactoryArea, pk=pk)
    area.is_active = False
    area.save()
    messages.success(request, f'厂区 {area.name} 已禁用')
    return redirect('factory_area:list')

def factory_area_enable(request, pk):
    """启用厂区"""
    area = get_object_or_404(FactoryArea, pk=pk)
    area.is_active = True
    area.save()
    messages.success(request, f'厂区 {area.name} 已启用')
    return redirect('factory_area:list')

# Line相关视图函数
def line_list(request):
    """线体列表"""
    lines = Line.objects.select_related('factory_area', 'floor').all()
    return render(request, 'factory_area/line_list.html', {'lines': lines})

def line_add(request):
    """新增线体"""
        # 检查线体名称是否唯一（全局唯一）
    factory_areas = FactoryArea.objects.filter(is_active=True)
    floors = Floor.objects.filter(is_active=True)

    if request.method == 'POST':
        # 获取表单数据
        line_name = request.POST.get('line_name', '').strip()
        factory_area_id = request.POST.get('factory_area', '')
        floor_id = request.POST.get('floor', '')
        owner_person_id = request.POST.get('owner_person_id', '').strip()
        
        # 验证必填字段
        if not line_name:
            messages.error(request, '线体名称不能为空')
        elif not factory_area_id:
            messages.error(request, '请选择所属厂区')
        elif not owner_person_id:
            messages.error(request, '责任人ID不能为空')
        else:
            try:
                factory_area = FactoryArea.objects.get(id=factory_area_id)
                
                # 检查线体名称是否唯一（全局唯一）
                if Line.objects.filter(line_name=line_name).exists():
                    messages.error(request, f'线体名称 {line_name} 已存在')
                else:
                    # 创建设备
                    line = Line.objects.create(
                        line_name=line_name,
                        factory_area=factory_area,
                        floor_id=floor_id if floor_id else None,
                        owner_person_id=owner_person_id,
                        is_active=True
                    )
                    messages.success(request, f'线体 {line_name} 创建成功')
                    return redirect('factory_area:line_list')
                    
            except FactoryArea.DoesNotExist:
                messages.error(request, '厂区不存在')
    
    # 如果是GET请求或者POST请求有错误，显示表单
    return render(request, 'factory_area/line_form.html', {
        'factory_areas': factory_areas,
        'floors': floors,
    })

    # factory_areas = FactoryArea.objects.filter(is_active=True)
    # floors = Floor.objects.filter(is_active=True)
    
    # if request.method == 'POST':
    #     line_code = request.POST.get('line_code')
    #     line_name = request.POST.get('line_name')
    #     factory_area_id = request.POST.get('factory_area')
    #     floor_id = request.POST.get('floor')
    #     owner_person_id = request.POST.get('owner_person_id')
        
    #     factory_area = FactoryArea.objects.get(id=factory_area_id)
        
    #     # 检查同一厂区内线体编码是否唯一
    #     if Line.objects.filter(factory_area=factory_area, line_code=line_code).exists():
    #         messages.error(request, f'厂区{factory_area.name}中已存在线体编码{line_code}')
    #     else:
    #         line = Line.objects.create(
    #             line_code=line_code,
    #             line_name=line_name,
    #             factory_area=factory_area,
    #             floor_id=floor_id if floor_id else None,
    #             owner_person_id=owner_person_id,
    #             is_active=True
    #         )
    #         messages.success(request, f'线体{line_name}创建成功')
    #         return redirect('factory_area:line_list')
    
    # return render(request, 'factory_area/line_form.html', {
    #     'factory_areas': factory_areas,
    #     'floors': floors
    # })

def line_edit(request, pk):
    """编辑线体"""
    line = get_object_or_404(Line, pk=pk)
    factory_areas = FactoryArea.objects.filter(is_active=True)
    floors = Floor.objects.filter(is_active=True)
    
    if request.method == 'POST':
        line_name = request.POST.get('line_name')
        factory_area_id = request.POST.get('factory_area')
        floor_id = request.POST.get('floor')
        owner_person_id = request.POST.get('owner_person_id')
        is_active = request.POST.get('is_active') == 'on'
        
        if not line_name:
            messages.error(request, '线体名称不能为空')
            return render(request, 'factory_area/line_form.html', {
                'line': line,
                'factory_areas': factory_areas,
                'floors': floors,
            })
        
        try:
            factory_area = FactoryArea.objects.get(id=factory_area_id)
            
            # 检查线体名称是否唯一（排除自己）
            if Line.objects.filter(line_name=line_name).exclude(pk=pk).exists():
                messages.error(request, f'线体名称 {line_name} 已存在')
            else:
                line.line_name = line_name
                line.factory_area = factory_area
                line.floor_id = floor_id if floor_id else None
                line.owner_person_id = owner_person_id
                line.is_active = is_active
                line.save()
                
                messages.success(request, f'线体{line_name}更新成功')
                return redirect('factory_area:line_list')
                
        except FactoryArea.DoesNotExist:
            messages.error(request, '厂区不存在')
    
    return render(request, 'factory_area/line_form.html', {
        'line': line,
        'factory_areas': factory_areas,
        'floors': floors,
    })

def line_disable(request, pk):
    """禁用线体"""
    line = get_object_or_404(Line, pk=pk)
    line.is_active = False
    line.save()
    messages.success(request, f'线体{line.line_name}已禁用')
    return redirect('factory_area:line_list')

def line_enable(request, pk):
    """启用电线体"""
    line = get_object_or_404(Line, pk=pk)
    line.is_active = True
    line.save()
    messages.success(request, f'线体{line.line_name}已启用')
    return redirect('factory_area:line_list')


# 设备类型相关视图
def equipment_type_list(request):
    """设备类型列表"""
    equipment_types = EquipmentType.objects.all().order_by('equipment_type_id')
    
    # 筛选功能
    device_category = request.GET.get('device_category')
    if device_category:
        equipment_types = equipment_types.filter(device_category=device_category)
    
    calibration_method = request.GET.get('calibration_method')
    if calibration_method:
        equipment_types = equipment_types.filter(calibration_method=calibration_method)
    
    search = request.GET.get('search')
    if search:
        equipment_types = equipment_types.filter(
            models.Q(equipment_type_id__icontains=search) |
            models.Q(name__icontains=search) |
            models.Q(brand__icontains=search) |
            models.Q(model__icontains=search)
        )
    
    return render(request, 'factory_area/equipment_type_list.html', {
        'equipment_types': equipment_types,
        'device_category_choices': EquipmentType.DEVICE_CATEGORY_CHOICES,
        'calibration_method_choices': EquipmentType.CALIBRATION_METHOD_CHOICES,
    })

def equipment_type_add(request):
    """新增设备类型"""
    if request.method == 'POST':
        equipment_type_id = request.POST.get('equipment_type_id')
        name = request.POST.get('name')
        device_category = request.POST.get('device_category')
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        calibration_method = request.POST.get('calibration_method')
        
        # 检查类型ID是否唯一
        if EquipmentType.objects.filter(equipment_type_id=equipment_type_id).exists():
            messages.error(request, f'设备类型ID {equipment_type_id} 已存在')
        else:
            # 创建设备类型
            equipment_type = EquipmentType.objects.create(
                equipment_type_id=equipment_type_id,
                name=name,
                device_category=device_category,
                brand=brand,
                model=model,
                calibration_method=calibration_method,
                is_active=True
            )
            
            messages.success(request, f'设备类型 {name} 创建成功')
            return redirect('factory_area:equipment_type_list')
    
    return render(request, 'factory_area/equipment_type_form.html', {
        'device_category_choices': EquipmentType.DEVICE_CATEGORY_CHOICES,
        'calibration_method_choices': EquipmentType.CALIBRATION_METHOD_CHOICES,
    })

def equipment_type_edit(request, pk):
    """编辑设备类型"""
    equipment_type = get_object_or_404(EquipmentType, pk=pk)
    
    if request.method == 'POST':
        equipment_type_id = request.POST.get('equipment_type_id')
        name = request.POST.get('name')
        device_category = request.POST.get('device_category')
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        calibration_method = request.POST.get('calibration_method')
        is_active = request.POST.get('is_active') == 'on'
        
        # 检查类型ID是否唯一（排除自己）
        if EquipmentType.objects.filter(equipment_type_id=equipment_type_id).exclude(pk=pk).exists():
            messages.error(request, f'设备类型ID {equipment_type_id} 已存在')
        else:
            equipment_type.equipment_type_id = equipment_type_id
            equipment_type.name = name
            equipment_type.device_category = device_category
            equipment_type.brand = brand
            equipment_type.model = model
            equipment_type.calibration_method = calibration_method
            equipment_type.is_active = is_active
            
            # 保存维保/校正规则
            equipment_type.maintenance_required = request.POST.get('maintenance_required') == 'on'
            equipment_type.calibration_required = request.POST.get('calibration_required') == 'on'
            equipment_type.maintenance_interval_days = request.POST.get('maintenance_interval_days') or 180
            equipment_type.calibration_interval_days = request.POST.get('calibration_interval_days') or 365
            equipment_type.maintenance_duration_min = request.POST.get('maintenance_duration_min') or 60
            equipment_type.calibration_duration_min = request.POST.get('calibration_duration_min') or 120
            
            # 保存成本信息
            estimated_unit_cost = request.POST.get('estimated_unit_cost')
            if estimated_unit_cost:
                equipment_type.estimated_unit_cost = estimated_unit_cost
            equipment_type.currency = request.POST.get('currency', 'CNY')
            equipment_type.cost_source = request.POST.get('cost_source', '')
            
            cost_updated_at = request.POST.get('cost_updated_at')
            if cost_updated_at:
                equipment_type.cost_updated_at = cost_updated_at
            
            equipment_type.save()
            
            messages.success(request, f'设备类型 {name} 更新成功')
            return redirect('factory_area:equipment_type_list')
    
    return render(request, 'factory_area/equipment_type_form.html', {
        'equipment_type': equipment_type,
        'device_category_choices': EquipmentType.DEVICE_CATEGORY_CHOICES,
        'calibration_method_choices': EquipmentType.CALIBRATION_METHOD_CHOICES,
    })

def equipment_type_disable(request, pk):
    """禁用设备类型"""
    equipment_type = get_object_or_404(EquipmentType, pk=pk)
    equipment_type.is_active = False
    equipment_type.save()
    messages.success(request, f'设备类型 {equipment_type.name} 已禁用')
    return redirect('factory_area:equipment_type_list')

def equipment_type_enable(request, pk):
    """启用设备类型"""
    equipment_type = get_object_or_404(EquipmentType, pk=pk)
    equipment_type.is_active = True
    equipment_type.save()
    messages.success(request, f'设备类型 {equipment_type.name} 已启用')
    return redirect('factory_area:equipment_type_list')


# 设备实例相关视图
def device_list(request):
    """设备实例列表"""
    devices = Device.objects.select_related('equipment_type', 'line').all()
    
    # 筛选功能
    equipment_type_id = request.GET.get('equipment_type')
    if equipment_type_id:
        devices = devices.filter(equipment_type_id=equipment_type_id)
    
    operational_state = request.GET.get('operational_state')
    if operational_state:
        devices = devices.filter(operational_state=operational_state)
    
    location_type = request.GET.get('location_type')
    if location_type:
        devices = devices.filter(location_type=location_type)
    
    department_name = request.GET.get('department_name')
    if department_name:
        devices = devices.filter(department_name__icontains=department_name)
    
    search = request.GET.get('search')
    if search:
        devices = devices.filter(
            models.Q(ppid__icontains=search) |
            models.Q(device_name__icontains=search) |
            models.Q(device_code__icontains=search) |
            models.Q(asset_tag__icontains=search) |
            models.Q(rfid_tag__icontains=search) |
            models.Q(keeper__icontains=search)
        )
    
    # 获取筛选选项
    equipment_types = EquipmentType.objects.filter(is_active=True)
    operational_state_choices = Device.OPERATIONAL_STATE_CHOICES
    location_type_choices = Device.LOCATION_TYPE_CHOICES
    
    # 获取部门列表（去重）
    departments = Device.objects.values_list('department_name', flat=True).distinct()
    
    return render(request, 'factory_area/device_list.html', {
        'devices': devices,
        'equipment_types': equipment_types,
        'operational_state_choices': operational_state_choices,
        'location_type_choices': location_type_choices,
        'departments': departments,
    })

def device_add(request):
    """新增设备实例"""
    equipment_types = EquipmentType.objects.filter(is_active=True)
    lines = Line.objects.filter(is_active=True)
    
    if request.method == 'POST':
        ppid = request.POST.get('ppid')
        
        # 检查PPID是否唯一
        if Device.objects.filter(ppid=ppid).exists():
            messages.error(request, f'PPID {ppid} 已存在')
        else:
            try:
                equipment_type_id = request.POST.get('equipment_type')
                equipment_type = EquipmentType.objects.get(id=equipment_type_id)
                
                # 检查设备类型是否启用
                if not equipment_type.is_active:
                    messages.error(request, '不能选择已禁用的设备类型')
                    return redirect('factory_area:device_add')
                
                # 创建设备
                device = Device(
                    ppid=ppid,
                    device_name=request.POST.get('device_name', ''),
                    device_code=request.POST.get('device_code', ''),
                    asset_tag=request.POST.get('asset_tag') or None,
                    equipment_type=equipment_type,
                    department_name=request.POST.get('department_name', ''),
                    keeper=request.POST.get('keeper', ''),
                    rfid_tag=request.POST.get('rfid_tag') or None,
                    inventory_external_id=request.POST.get('inventory_external_id') or None,
                    operational_state=request.POST.get('operational_state', 'IDLE'),
                    location_type=request.POST.get('location_type', 'OTHER'),
                    location_text=request.POST.get('location_text', ''),
                    area=request.POST.get('area', ''),
                    is_active=True
                )
                
                # 处理RFID纳入时间
                rfid_enrolled_at = request.POST.get('rfid_enrolled_at')
                if rfid_enrolled_at:
                    device.rfid_enrolled_at = rfid_enrolled_at
                
                # 处理线体关联
                line_id = request.POST.get('line')
                if line_id:
                    device.line_id = line_id
                
                # 检查RFID唯一性
                rfid_tag = request.POST.get('rfid_tag')
                if rfid_tag and Device.objects.filter(rfid_tag=rfid_tag).exists():
                    messages.error(request, f'RFID标签 {rfid_tag} 已存在')
                    return redirect('factory_area:device_add')
                
                device.save()
                messages.success(request, f'设备 {device.get_device_display_name()} 创建成功')
                return redirect('factory_area:device_list')
                
            except EquipmentType.DoesNotExist:
                messages.error(request, '设备类型不存在')
    
    return render(request, 'factory_area/device_form.html', {
        'equipment_types': equipment_types,
        'lines': lines,
        'operational_state_choices': Device.OPERATIONAL_STATE_CHOICES,
        'location_type_choices': Device.LOCATION_TYPE_CHOICES,
    })

def device_edit(request, pk):
    """编辑设备实例"""
    device = get_object_or_404(Device, pk=pk)
    equipment_types = EquipmentType.objects.filter(is_active=True)
    lines = Line.objects.filter(is_active=True)
    
    if request.method == 'POST':
        ppid = request.POST.get('ppid')
        
        # 检查PPID是否唯一（排除自己）
        if Device.objects.filter(ppid=ppid).exclude(pk=pk).exists():
            messages.error(request, f'PPID {ppid} 已存在')
        else:
            try:
                equipment_type_id = request.POST.get('equipment_type')
                equipment_type = EquipmentType.objects.get(id=equipment_type_id)
                
                # 检查设备类型是否启用
                if not equipment_type.is_active and request.POST.get('is_active') == 'on':
                    messages.error(request, '不能将设备关联到已禁用的设备类型')
                    return redirect('factory_area:device_edit', pk=pk)
                
                # 更新设备信息
                device.ppid = ppid
                device.device_name = request.POST.get('device_name', '')
                device.device_code = request.POST.get('device_code', '')
                device.asset_tag = request.POST.get('asset_tag') or None
                device.equipment_type = equipment_type
                device.department_name = request.POST.get('department_name', '')
                device.keeper = request.POST.get('keeper', '')
                device.operational_state = request.POST.get('operational_state', 'IDLE')
                device.location_type = request.POST.get('location_type', 'OTHER')
                device.location_text = request.POST.get('location_text', '')
                device.area = request.POST.get('area', '')
                device.is_active = request.POST.get('is_active') == 'on'
                
                # 处理RFID相关字段
                rfid_tag = request.POST.get('rfid_tag')
                if rfid_tag:
                    # 检查RFID唯一性（排除自己）
                    if Device.objects.filter(rfid_tag=rfid_tag).exclude(pk=pk).exists():
                        messages.error(request, f'RFID标签 {rfid_tag} 已存在')
                        return redirect('factory_area:device_edit', pk=pk)
                    device.rfid_tag = rfid_tag
                else:
                    device.rfid_tag = None
                
                device.inventory_external_id = request.POST.get('inventory_external_id') or None
                
                rfid_enrolled_at = request.POST.get('rfid_enrolled_at')
                if rfid_enrolled_at:
                    device.rfid_enrolled_at = rfid_enrolled_at
                else:
                    device.rfid_enrolled_at = None
                
                # 处理线体关联
                line_id = request.POST.get('line')
                if line_id:
                    device.line_id = line_id
                else:
                    device.line = None
                
                device.save()
                messages.success(request, f'设备 {device.get_device_display_name()} 更新成功')
                return redirect('factory_area:device_list')
                
            except EquipmentType.DoesNotExist:
                messages.error(request, '设备类型不存在')
    
    return render(request, 'factory_area/device_form.html', {
        'device': device,
        'equipment_types': equipment_types,
        'lines': lines,
        'operational_state_choices': Device.OPERATIONAL_STATE_CHOICES,
        'location_type_choices': Device.LOCATION_TYPE_CHOICES,
    })

def device_disable(request, pk):
    """禁用设备"""
    device = get_object_or_404(Device, pk=pk)
    device.is_active = False
    device.save()
    messages.success(request, f'设备 {device.get_device_display_name()} 已禁用')
    return redirect('factory_area:device_list')

def device_enable(request, pk):
    """启用设备"""
    device = get_object_or_404(Device, pk=pk)
    # 检查设备类型是否启用
    if not device.equipment_type.is_active:
        messages.error(request, '设备类型已禁用，无法启用此设备')
        return redirect('factory_area:device_list')
    
    device.is_active = True
    device.save()
    messages.success(request, f'设备 {device.get_device_display_name()} 已启用')
    return redirect('factory_area:device_list')

def device_detail(request, pk):
    """设备详情"""
    device = get_object_or_404(Device, pk=pk)
    return render(request, 'factory_area/device_detail.html', {'device': device})


# 设备纳管配置相关视图
def maintenance_profile_list(request):
    """设备纳管配置列表"""
    # 获取筛选参数
    enable_maintenance = request.GET.get('enable_maintenance')
    use_type_defaults = request.GET.get('use_type_defaults')
    device_category = request.GET.get('device_category')

    # 构建查询
    profiles = DeviceMaintenanceProfile.objects.select_related(
        'device', 'device__equipment_type'
    ).all()

    if enable_maintenance is not None:
        profiles = profiles.filter(enable_maintenance=(enable_maintenance == 'true'))

    if use_type_defaults is not None:
        profiles = profiles.filter(use_type_defaults=(use_type_defaults == 'true'))

    if device_category:
        profiles = profiles.filter(device__equipment_type__device_category=device_category)

    # 获取设备类别选项用于筛选
    device_category_choices = EquipmentType.DEVICE_CATEGORY_CHOICES

    # 统计信息
    total_count = profiles.count()
    enabled_count = profiles.filter(enable_maintenance=True).count()
    disabled_count = profiles.filter(enable_maintenance=False).count()
    override_count = profiles.filter(use_type_defaults=False).count()

    return render(request, 'factory_area/maintenance_profile_list.html', {
        'profiles': profiles,
        'device_category_choices': device_category_choices,
        'total_count': total_count,
        'enabled_count': enabled_count,
        'disabled_count': disabled_count,
        'override_count': override_count,
    })


def maintenance_profile_edit(request, device_id):
    """编辑设备纳管配置"""
    device = get_object_or_404(Device, pk=device_id)
    profile, created = DeviceMaintenanceProfile.objects.get_or_create(
        device=device,
        defaults={
            'use_type_defaults': True,
            'enable_maintenance': True,
            'status': True,
        }
    )

    if request.method == 'POST':
        profile.enable_maintenance = request.POST.get('enable_maintenance') == 'on'
        profile.use_type_defaults = request.POST.get('use_type_defaults') == 'on'
        profile.status = request.POST.get('status') == 'on'

        if not profile.use_type_defaults:
            # 单台覆盖值
            profile.maintenance_required = request.POST.get('maintenance_required') == 'on'
            profile.calibration_required = request.POST.get('calibration_required') == 'on'
            profile.maintenance_interval_days = int(request.POST.get('maintenance_interval_days', 180))
            profile.calibration_interval_days = int(request.POST.get('calibration_interval_days', 365))
            profile.maintenance_duration_min = int(request.POST.get('maintenance_duration_min', 60))
            profile.calibration_duration_min = int(request.POST.get('calibration_duration_min', 120))

        profile.last_updated_by = request.user.username if request.user.is_authenticated else 'system'
        profile.save()

        messages.success(request, f'设备 {device.ppid} 的纳管配置已更新')
        return redirect('factory_area:maintenance_profile_list')

    return render(request, 'factory_area/maintenance_profile_form.html', {
        'device': device,
        'profile': profile,
    })


def maintenance_profile_batch_create(request):
    """批量创建纳管配置"""
    if request.method == 'POST':
        equipment_type_id = request.POST.get('equipment_type_id')

        if not equipment_type_id:
            messages.error(request, '请选择设备类型')
            return redirect('factory_area:maintenance_profile_batch_create')

        equipment_type = get_object_or_404(EquipmentType, pk=equipment_type_id)

        # 查找该类型下没有纳管配置的设备
        devices_without_profile = Device.objects.filter(
            equipment_type=equipment_type,
            is_active=True
        ).exclude(
            maintenance_profile__isnull=False
        )

        count = 0
        for device in devices_without_profile:
            DeviceMaintenanceProfile.objects.create(
                device=device,
                use_type_defaults=True,
                enable_maintenance=True,
                status=True,
            )
            count += 1

        messages.success(request, f'已为 {count} 台设备创建纳管配置')
        return redirect('factory_area:maintenance_profile_list')

    equipment_types = EquipmentType.objects.filter(is_active=True)
    return render(request, 'factory_area/maintenance_profile_batch_create.html', {
        'equipment_types': equipment_types,
    })


def maintenance_profile_batch_reset(request):
    """批量恢复默认继承"""
    if request.method == 'POST':
        equipment_type_id = request.POST.get('equipment_type_id')

        if not equipment_type_id:
            messages.error(request, '请选择设备类型')
            return redirect('factory_area:maintenance_profile_batch_reset')

        equipment_type = get_object_or_404(EquipmentType, pk=equipment_type_id)

        # 重置该类型下所有设备的纳管配置为继承模式
        count = DeviceMaintenanceProfile.objects.filter(
            device__equipment_type=equipment_type
        ).update(
            use_type_defaults=True,
            last_updated_by=request.user.username if request.user.is_authenticated else 'system'
        )

        messages.success(request, f'已重置 {count} 台设备的纳管配置为继承模式')
        return redirect('factory_area:maintenance_profile_list')

    equipment_types = EquipmentType.objects.filter(is_active=True)
    return render(request, 'factory_area/maintenance_profile_batch_reset.html', {
        'equipment_types': equipment_types,
    })