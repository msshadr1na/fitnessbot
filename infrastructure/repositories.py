class SettingsRepository:
    def __init__(self, pool):
        self.pool = pool

    async def create(self, settings):
        sql = "INSERT INTO settings (notification_settings) VALUES ($1) RETURNING id"
        row = await self.pool.fetchrow(sql, settings.notification_settings)

        settings.id = row["id"]
        return settings
