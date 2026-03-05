from infrastructure.repositories import BookingRepository, UserRepository, SettingsRepository, OrganizationRepository, OrganizationMemberRepository, TrainingRepository
from app.models import Settings, User, Organization, OrganizationMember

class UserService:
    def __init__(self, user_repository : UserRepository, settings_repository: SettingsRepository):
        self.user_repository = user_repository
        self.settings_repository = settings_repository

    async def find_by_tgid(self, telegram_id):
        return await self.user_repository.find(telegram_id)

    async def registration(self, telegram_id, phone, first_name, last_name, middle_name):
        default_settings = Settings(id=None, notification_settings={"before_hour": 0, "before_day": 1})
        saved_settings = await self.settings_repository.create(default_settings)
        newUser = User(None, telegram_id, phone, first_name, last_name, saved_settings.id, middle_name)
        return await self.user_repository.create(newUser)

class OrganizationService:
    def __init__(self, organization_repository : OrganizationRepository, organizationMember_repository : OrganizationMemberRepository):
        self.organization_repository = organization_repository
        self.organizationMember_repository = organizationMember_repository

# Поиск организации по названию
    async def find_by_name(self, name):
        return await self.organization_repository.find_by_name(name)

    async def get_by_id(self,id):
        organization = await self.organization_repository.find_by_id(id)
        return organization

# Создание организации (добавление в бд)
    async def create_organization(self, user: User, name):
        newOrganization = Organization(None,name)
        savedOrganization = await self.organization_repository.create(newOrganization)
        newOrganizationMember = OrganizationMember(None,user.id,1,savedOrganization.id)
        owner = await self.organizationMember_repository.create(newOrganizationMember)
        return savedOrganization

# Удаление организации и всех зависимостей
    async def delete_organization(self, user_id, org_id):      
        organization = await self.organization_repository.find_by_id(org_id)
        if not organization:
            raise ValueError("Организация не найдена")

        organization = await self.organization_repository.delete(org_id)
        return organization

# Просмотр организаций, которыми пользователь владеет
    async def show_owned_orgs(self,user_id):
        org_ids = await self.organizationMember_repository.get_membered_orgs(user_id, 1)
        names = await self.organizationMember_repository.get_names_by_ids(org_ids)
        return org_ids, names

# Редактирование созданной организации



