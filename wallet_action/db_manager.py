from tortoise import Tortoise, fields
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.IntField(unique=True)
    wallets = fields.ManyToManyField('models.Wallet', related_name='walets',
                                     through='user_wallets')


class Wallet(Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=42, unique=True)
    users = fields.ManyToManyField('models.User', related_name='users',
                                   through='wallet_users')


async def init_db():
    await Tortoise.init(
        db_url='postgres://kem:Vmf152@localhost/telegrammbot',
        modules={'models': ['wallet_action.db_manager']}
    )
    await Tortoise.generate_schemas()
