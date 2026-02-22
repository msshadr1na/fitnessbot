from infrastructure.repositories import UserRepository, SettingsRepository, OrganizationRepository, OrganizationMemberRepository
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

class OrganiationService:
    def __init__(self, organization_repository : OrganizationRepository, organizationMember_repository : OrganizationMemberRepository):
        self.organization_repository = organization_repository
        self.organizationMember_repository = organizationMember_repository

    async def find_by_name(self, name):
        return await self.organization_repository.find_by_name(name)

    async def create_organization(self, user: User, name):
        newOrganization = Organization(None,name)
        savedOrganization = await self.organization_repository.create(newOrganization)
        newOrganizationMember = OrganizationMember(None,user.id,1,savedOrganization.id)
        owner = await self.organizationMember_repository.create(newOrganizationMember)
        return savedOrganization

    # Поиск организаций с таким же именем, чтобы нельзя было повторяться
    # Удаление организации
    # Просмотр организаций, которыми пользователь владеет
    # Редактирование созданной организации



