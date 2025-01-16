
from dataclasses import dataclass, field, asdict
from typing import Optional, Any, Dict, List



@dataclass
class Base:
    def __getitem__(self, item):
        return getattr(self, item)

    def __getattr__(self, item):
        for field in self.__dataclass_fields__.values():
            value = getattr(self, field.name)
            if isinstance(value, Base):
                try:
                    return value[item]
                except AttributeError:
                    continue
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def get(self, key, default=None):
        return self.__dict__.get(key, default)
    
    def to_dict(self):
        return asdict(self)
    

def dict_to_dataclass(data_class, data):
    if isinstance(data, dict):
        field_types = {f.name: f.type for f in data_class.__dataclass_fields__.values()}
        kwargs = {}
        for key, value in data.items():
            if key in field_types:
                if hasattr(field_types[key], '__dataclass_fields__'):
                    kwargs[key] = dict_to_dataclass(field_types[key], value)
                else:
                    kwargs[key] = value
        return data_class(**kwargs)
    return data_class()


@dataclass
class Requirements(Base):
    hardware: Optional[str] = None
    hardware_type: Optional[str] = None
    memory: Optional[str] = None
    preferred_cp_list: Optional[Any] = None
    region: Optional[str] = None
    storage: Optional[str] = None
    update_max_lag: Optional[Any] = None
    vcpu: Optional[str] = None

@dataclass
class Config(Base):
    description: Optional[str] = None
    hardware: Optional[str] = None
    hardware_id: Optional[int] = None
    hardware_type: Optional[str] = None
    memory: Optional[int] = None
    name: Optional[str] = None
    price_per_hour: Optional[float] = None
    vcpu: Optional[int] = None

@dataclass
class ActiveOrder(Base):
    config: Optional[Config] = None

@dataclass
class Space(Base):
    activeOrder: Optional[ActiveOrder] = None
    name: Optional[str] = None
    uuid: Optional[str] = None

@dataclass
class TaskDetail(Base):
    amount: Optional[float] = None
    bidder_limit: Optional[int] = None
    created_at: Optional[int] = None
    dcc_selected_cp_list: Optional[Any] = None
    duration: Optional[int] = None
    end_at: Optional[int] = None
    hardware: Optional[str] = None
    hardware_id: Optional[int] = None
    job_result_uri: Optional[str] = None
    job_source_uri: Optional[str] = None
    price_per_hour: Optional[str] = None
    requirements: Optional[Requirements] = None
    space: Optional[Space] = None
    start_at: Optional[int] = None
    status: Optional[str] = None
    storage_source: Optional[str] = None
    type: Optional[str] = None
    updated_at: Optional[int] = None
    ip_whitelist: Optional[List[str]] = None

@dataclass
class Task(Base):
    comments: Optional[str] = None
    created_at: Optional[int] = None
    end_at: Optional[int] = None
    id: Optional[int] = None
    leading_job_id: Optional[str] = None
    name: Optional[str] = None
    refund_amount: Optional[str] = None
    refund_wallet: Optional[str] = None
    source: Optional[str] = None
    start_at: Optional[int] = None
    start_in: Optional[int] = None
    status: Optional[str] = None
    task_detail: TaskDetail = field(default_factory=TaskDetail)
    task_detail_cid: Optional[str] = None
    tx_hash: Optional[Any] = None
    type: Optional[str] = None
    updated_at: Optional[int] = None
    user_id: Optional[int] = None
    uuid: Optional[str] = None

@dataclass
class ConfigOrder(Base):
    config_id: Optional[int] = None
    created_at: Optional[int] = None
    duration: Optional[int] = None
    ended_at: Optional[int] = None
    error_code: Optional[int] = None
    id: Optional[int] = None
    order_type: Optional[str] = None
    preferred_cp_list: Optional[Any] = None
    refund_tx_hash: Optional[str] = None
    region: Optional[str] = None
    space_id: Optional[str] = None
    start_in: Optional[int] = None
    started_at: Optional[int] = None
    status: Optional[str] = None
    task_uuid: Optional[str] = None
    tx_hash: Optional[str] = None
    updated_at: Optional[int] = None
    uuid: Optional[str] = None

@dataclass
class TaskCreationResult(Base):
    task: Task = field(default_factory=Task)
    config_order: ConfigOrder = field(default_factory=ConfigOrder)
    tx_hash: Optional[str] = None
    tx_hash_approve: Optional[str] = None
    task_uuid: Optional[str] = None
    instance_type: Optional[str] = None
    price: Optional[float] = None
    duration: Optional[int] = None
    job_source_uri: Optional[str] = None
    wallet_address: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None

    @staticmethod
    def load_from_resp(result: Dict[str, Any]) -> 'TaskCreationResult':
        try:
            data = result.get('data', {})
            task_data = data.get('task') if data else {}
            task = dict_to_dataclass(Task, task_data) if task_data else Task()

            config_order_data = result.get('config_order')
            config_order = dict_to_dataclass(ConfigOrder, config_order_data) if config_order_data else ConfigOrder()

            return TaskCreationResult(
                task=task,
                config_order=config_order,
                tx_hash=result.get('tx_hash'),
                task_uuid=result.get('task_uuid'),
                instance_type=result.get('instance_type'),
                price=result.get('price'),
                duration=config_order.duration,
                job_source_uri=task.task_detail.job_source_uri,
                wallet_address=task.refund_wallet,
                status=result.get('status'),
                message=result.get('message')
            )
        except Exception as e:
            raise ValueError(f"An error occurred while loading TaskCreationResult: {e}")

@dataclass
class CPAccount(Base):
    beneficiary: Optional[str] = None
    cp_account_address: Optional[str] = None
    created_at: Optional[int] = None
    freeze_online: Optional[Any] = None
    id: Optional[int] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    multi_address: Optional[List[str]] = None
    name: Optional[str] = None
    node_id: Optional[str] = None
    online: Optional[int] = None
    owner_address: Optional[str] = None
    region: Optional[str] = None
    task_types: Optional[str] = None
    updated_at: Optional[int] = None
    version: Optional[str] = None
    worker_address: Optional[str] = None

@dataclass
class Job(Base):
    build_log: Optional[str] = None
    comments: Optional[str] = None
    container_log: Optional[str] = None
    cp_account_address: Optional[str] = None
    created_at: Optional[int] = None
    duration: Optional[int] = None
    ended_at: Optional[int] = None
    hardware: Optional[str] = None
    id: Optional[int] = None
    job_real_uri: Optional[str] = None
    job_result_uri: Optional[str] = None
    job_source_uri: Optional[str] = None
    name: Optional[str] = None
    node_id: Optional[str] = None
    start_at: Optional[int] = None
    status: Optional[str] = None
    storage_source: Optional[str] = None
    task_uuid: Optional[str] = None
    type: Optional[Any] = None
    updated_at: Optional[int] = None
    uuid: Optional[str] = None

@dataclass
class TaskInfo(Base):
    computing_providers: Optional[List[CPAccount]] = field(default_factory=list)
    config_orders: Optional[List[ConfigOrder]] = field(default_factory=list)
    jobs: Optional[List[Job]] = field(default_factory=list)
    task: Optional[Task] = field(default_factory=Task)

    def __init__(self, data: Dict[str, Any]):
        task_data = data.get('task') if data else {}
        self.task = dict_to_dataclass(Task, task_data) if task_data else Task()

        computing_providers_data = data.get('computing_providers', []) if data else []
        self.computing_providers = [dict_to_dataclass(CPAccount, cp) for cp in computing_providers_data]

        config_orders_data = data.get('config_orders', []) if data else []
        self.config_orders = [dict_to_dataclass(ConfigOrder, config_order) for config_order in config_orders_data]

        jobs_data = data.get('jobs', []) if data else []
        self.jobs = [dict_to_dataclass(Job, job) for job in jobs_data]
        

@dataclass
class TaskDeploymentInfo(Base):
    computing_providers: Optional[List[CPAccount]] = field(default_factory=list)
    config_orders: Optional[List[ConfigOrder]] = field(default_factory=list)
    jobs: Optional[List[Job]] = field(default_factory=list)
    task: Optional[Task] = field(default_factory=Task)
    status: Optional[str] = None
    message: Optional[str] = None
    
    @staticmethod
    def load_from_resp(result: Dict[str, Any]) -> 'TaskDeploymentInfo':
        try:
            data = result.get('data', {})
            task_info = TaskInfo(data)
            return TaskDeploymentInfo(
                task=task_info.task,
                computing_providers=task_info.computing_providers,
                config_orders=task_info.config_orders,
                jobs=task_info.jobs,
                status=result.get('status'),
                message=result.get('message')
            )
        except Exception as e:
            raise ValueError(f"An error occurred while loading TaskDeploymentInfo: {e}")


@dataclass
class TaskList(Base):
    task_list: Optional[List[TaskInfo]] = field(default_factory=list)
    page: Optional[int] = None
    size: Optional[int] = None
    total: Optional[int] = None
    total_page: Optional[int] = None
    status: Optional[str] = None
    message: Optional[str] = None

    @staticmethod
    def load_from_resp(result: Dict[str, Any]) -> 'TaskList':
        try:
            data = result.get('data', {})
            _list = data.get('list') if data else []
            page = data.get('page') if data else None
            size = data.get('size') if data else None
            total = data.get('total') if data else None
            total_page = data.get('total_page') if data else None

            task_list = []
            for _task_data in _list:
                if _task_data and isinstance(_task_data, dict):
                    task_list.append(TaskInfo(
                        **_task_data
                    ))

            return TaskList(
                task_list=task_list,
                page=page,
                size=size,
                total=total,
                total_page=total_page,
                status=result.get('status'),
                message=result.get('message')
            )
        except Exception as e:
            raise ValueError(f"An error occurred while loading TaskList: {e}")

@dataclass
class TaskRenewalResult(Base):
    config_order: Optional[ConfigOrder] = field(default_factory=ConfigOrder)
    task: Optional[Task] = field(default_factory=Task)
    task_uuid: Optional[str] = None
    tx_hash_approve: Optional[str] = None
    tx_hash: Optional[str] = None
    price: Optional[float] = None
    status: Optional[str] = None
    message: Optional[str] = None

    @staticmethod
    def load_from_resp(result: Dict[str, Any]) -> 'TaskRenewalResult':
        try:
            data = result.get('data', {})
            task_data = data.get('task') if data else {}
            task = dict_to_dataclass(Task, task_data) if task_data else Task()

            config_order_data = data.get('config_order') if data else {}
            config_order = dict_to_dataclass(ConfigOrder, config_order_data) if config_order_data else ConfigOrder()

            return TaskRenewalResult(
                task=task,
                config_order=config_order,
                task_uuid=result.get('task_uuid'),
                tx_hash=result.get('tx_hash'),
                status=result.get('status'),
                message=result.get('message')
            )
        except Exception as e:
            raise ValueError(f"An error occurred while loading RenewTaskResp: {e}")

@dataclass
class TaskTerminationMessage(Base):
    retryable: Optional[bool] = None
    task_status: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None

    @staticmethod
    def load_from_resp(result: Dict[str, Any]) -> 'TaskTerminationMessage':
        try:
            data = result.get('data', {})
            return TaskTerminationMessage(
                retryable=data.get('retryable') if data else None,
                task_status=data.get('task_status') if data else None,
                status=result.get('status'),
                message=result.get('message')
            )
        except Exception as e:
            raise ValueError(f"An error occurred while loading TaskTerminationMessage: {e}")

@dataclass
class PaymentResult(Base):
    tx_hash_approve: Optional[str] = None
    tx_hash: Optional[str] = None
    amount: Optional[float] = None

@dataclass
class GPUCount(Base):
    gpu_model: Optional[str] = None
    max_count: Optional[int] = None
    region: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in super().to_dict().items() if v is not None}

@dataclass
class GPUSelectionList(Base):
    gpu_list: Optional[List[GPUCount]] = field(default_factory=list)

    @staticmethod
    def load_from_resp(result: Dict[str, Any]) -> 'GPUSelectionList':
        try:
            data = result.get('data', {})
            _list = data.get('gpus') if data else []

            gpu_list = []
            for _task_data in _list:
                if _task_data and isinstance(_task_data, dict):
                    gpu_list.append(GPUCount(
                        **_task_data
                    ))

            return GPUSelectionList(
                gpu_list=gpu_list
            )
        except Exception as e:
            raise ValueError(f"An error occurred while loading GPUSelectionList: {e}")
        
    def to_dict(self):
        gpu_list = [gpu.to_dict() for gpu in self.gpu_list]
        return {
            'gpu_list': gpu_list
        }
        

@dataclass
class CustomInstance(Base):
    cpu: Optional[int] = None
    gpu_count: Optional[int] = None
    gpu_model: Optional[str] = None
    memory: Optional[int] = None
    region: Optional[str] = None
    storage: Optional[int] = None

@dataclass
class CustomInstanceResult(Base):
    available: Optional[bool] = None
    custom_instance: Optional[CustomInstance] = field(default_factory=CustomInstance)
    price_expiry_time: Optional[str] = None
    price_per_hour: Optional[float] = None

    @staticmethod
    def load_from_resp(result: Dict[str, Any]) -> 'CustomInstanceResult':
        try:
            data = result.get('data', {})
            custom_instance = data.get('custom_instance') if data else {}
            custom_instance = dict_to_dataclass(CustomInstance, custom_instance) if custom_instance else CustomInstance()

            return CustomInstanceResult(
                available=data.get('available'),
                custom_instance=custom_instance,
                price_expiry_time=data.get('price_expiry_time'),
                price_per_hour=data.get('price_per_hour')
            )
        except Exception as e:
            raise ValueError(f"An error occurred while loading ConfigResponse: {e}")