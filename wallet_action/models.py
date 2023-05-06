from tortoise import Tortoise, fields
from tortoise.models import Model
from datetime import datetime, timedelta


class User(Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.IntField(unique=True)
    trial_ends_at = fields.DatetimeField(
        default=datetime.now() + timedelta(days=14)
    )
    paid_subscription = fields.BooleanField(default=False)
    wallets = fields.ManyToManyField('models.Wallet', related_name='walets',
                                     through='user_wallets')


class Wallet(Model):
    id = fields.IntField(pk=True)
    address = fields.CharField(max_length=42, unique=True)


async def init_db():
    await Tortoise.init(
        db_url='postgres://kem:Vmf152@localhost/telegrammbot',
        modules={'models': ['wallet_action.models']}
    )
    await Tortoise.generate_schemas()
