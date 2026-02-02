from app.models import Settings, TrainingType, Training, User, OrganizationMember, Organization, Gym, Booking, Review

class SettingsRepository:
    def __init__(self, pool):
        self.pool = pool

    async def create(self, settings: Settings):
        sql = "insert into settings (notification_settings) values ($1) returning id"
        row = await self.pool.fetchrow(sql, settings.notification_settings)

        settings.id = row["id"]
        return settings

class UserRepository:
    def __init__(self, pool):
        self.pool = pool

    async def create(self, user: User):
        sql = """insert into users (telegram_id, phone, first_name, last_name, middle_name, settings_id) values 
        ($1, $2, $3, $4, $5, $6)"""
        row = await self.pool.fetchrow(sql, user.telegram_id, user.phone, user.first_name, user.last_name, user.middle_name, user.settings_id)
        user.id = row["id"]
        return user

    async def find(self, telegram_id):
        sql = "select * from users where telegram_id = $1"
        row = await self.pool.fetchrow(sql,telegram_id)

        if not row:
            return None
        else:            
            user = User(row["id"], row["telegram_id"], row["phone"], row["first_name"], row["last_name"], row["middle_name"], row["settings_id"])
            return user

    async def update(self,user):
        sql = "update users set phone = $2, first_name = $3, last_name = $4, middle_name = $5, settings_id = $6 where id = $1"

        await self.pool.execute(sql, user.id, user.phone, user.first_name, user.last_name, user.middle_name, user.settings_id)

class OrganizationMemberRepository:
    def __init__(self,pool):
        self.pool = pool

    async def create(self,member: OrganizationMember):
        sql = "insert into organization_member (user_id, role_id, organization_id) values ($1, $2, $3) returning id"
        row = await self.pool.fetchrow(sql, member.user_id, member.role_id, member.organization_id)

        member.id = row["id"]
        return member

class GymRepository:
    def __init__(self,pool):
        self.pool = pool

    async def create(self,gym: Gym):
        sql ="insert into gym (name, organization_id) values ($1, $2) returning id"
        row = await self.pool.fetchrow(sql, gym.name, gym.organization_id)

        gym.id = row["id"]
        return gym

class OrganizationRepository:
    def __init__(self, pool):
        self.pool = pool

    async def create(self, organization: Organization):
        sql ="insert into organization (name) values ($1) returning id"
        row = await self.pool.fetchrow(sql, organization.name)

        organization.id = row["id"]
        return organization

class TrainingRepository:
    def __init__(self,pool):
        self.pool = pool

    async def create(self,training: Training):
        sql = "insert into training (organization_id, gym_id, trainer_id, date_start, date_end, type_id, max_clients) values ($1, $2, $3, $4, $5, $6, $7) returning id"
        row = await self.pool.fetchrow(sql, training.organization_id, training.gym_id, training.trainer_id, training.date_start, training.date_end, training.type_id, training.max_clients)

        training.id = row["id"]
        return training

class BookingRepository:
    def __init__(self,pool):
        self.pool = pool

    async def create(self, booking:Booking):
        sql ="insert into booking (user_id, training_id, created_at) values ($1, $2, $3) returning id"
        row = await self.pool.fetchrow(sql, booking.user_id, booking.training_id, booking.created_at)

        booking.id = row["id"]
        return booking

class ReviewRepository:
    def __init__(self,pool):
        self.pool = pool

    async def create(self, review: Review):
        sql = "insert into review (user_id, training_id, grade, text) values ($1, $2, $3, $4) returning id"
        row = await self.pool.fetchrow(sql, review.user_id, review.training_id, review.grade, review.text)

        review.id = row["id"]
        return review