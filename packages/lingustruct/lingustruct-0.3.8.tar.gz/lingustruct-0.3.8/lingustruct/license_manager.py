import json
import os
import redis.asyncio as redis
from typing import Optional, Dict

class LicenseManager:
    def __init__(self, redis_client: redis.Redis):
        """Redis クライアントの初期化"""
        self.redis_client = redis_client

    async def check_connection(self):
        """Redisへの接続テスト"""
        try:
            is_connected = await self.redis_client.ping()
            if is_connected:
                print("Redis connection successful")
                return {"status": "success", "message": "Redis connection successful"}
            else:
                raise ValueError("Redis ping failed")
        except redis.ConnectionError as e:
            raise ValueError(f"Redis connection failed: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")

    async def validate_api_key(self, api_key: str) -> Optional[dict]:
        """APIキーの検証"""
        try:
            # Redisから `USER_PLAN:{api_key}`形式で取得
            key = f"USER_PLAN:{api_key}"
            user_info_json = await self.redis_client.get(key)
            if not user_info_json:
                raise ValueError("Invalid API key.")
            return json.loads(user_info_json)
        except redis.ConnectionError as e:
            raise ValueError(f"Redis connection error: {str(e)}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")

    async def add_license(self, api_key: str, user_info: dict):
        """ライセンスの追加"""
        try:
            key = f"USER_PLAN:{api_key}"
            if await self.redis_client.get(key):
                raise ValueError("API key already exists.")
            await self.redis_client.set(key, json.dumps(user_info))
        except redis.ConnectionError as e:
            raise ValueError(f"Redis connection error: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to add license: {str(e)}")

    async def remove_license(self, api_key: str):
        """ライセンスの削除"""
        try:
            key = f"USER_PLAN:{api_key}"
            await self.redis_client.delete(key)
        except redis.ConnectionError as e:
            raise ValueError(f"Redis connection error: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to remove license: {str(e)}")

async def validate_license_key(api_key: str, license_manager: LicenseManager) -> dict:
    """
    APIキーの検証を行い、ユーザー情報を返す関数。

    Args:
        api_key (str): 検証するAPIキー。
        license_manager (LicenseManager): LicenseManagerのインスタンス。

    Returns:
        dict: ユーザー情報。

    Raises:
        ValueError: APIキーが無効な場合やその他のエラー。
    """
    user_info = await license_manager.validate_api_key(api_key)
    if not user_info:
        raise ValueError("Invalid API key.")
    return user_info
