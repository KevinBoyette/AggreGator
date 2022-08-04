import enum


class AssetType(enum.Enum):
    STOCK = "Stock"
    CRYPTO = "Crypto"
    REIT = "REIT"
    IRA = "IRA"
    _401K = "401K"
    HSA = "HSA"
