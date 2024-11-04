from fastapi import HTTPException, status, Request
from typing import Dict
import time
import redis.asyncio as redis

class RateLimiter:
    def __init__(self, free_calls: int = 5, period: int = 3600, redis_client: redis.Redis = None):
        self.free_calls = free_calls  # 無料ユーザーのリクエスト上限
        self.period = period  # 期間（秒単位）
        self.redis_client = redis_client  # Redisクライアント

    async def enforce_limit(self, request: Request, user: Dict):
        """ユーザーのプランに基づき、レート制限を適用する"""
        ip = request.client.host

        # 有料ユーザーは無制限アクセスを許可
        if user.get("plan") == "paid":
            print(f"Paid user: Unlimited access for IP {ip}")
            return

        # 無料ユーザーはIPアドレスごとのアクセス制限を適用
        await self._check_ip_rate_limit(ip)

    async def _check_ip_rate_limit(self, ip: str):
        """IPアドレスに基づく無料ユーザーのレート制限"""
        current_time = int(time.time())
        key = f"RATE_LIMIT:{ip}"
        try:
            # トークンの残数を取得
            remaining = await self.redis_client.get(key)
            if remaining is None:
                # 初回リクエストの場合、カウントを1に初期化し、期限を設定
                await self.redis_client.set(key, self.free_calls - 1, ex=self.period)
                return
            remaining = int(remaining)
            if remaining <= 0:
                print(f"Rate limit exceeded for IP {ip}")
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded. Try again later."
                )
            else:
                # リクエスト数を減らす
                await self.redis_client.decr(key)
        except redis.RedisError as e:
            # Redisのエラーはサーバーエラーとして扱う
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Rate limiter service unavailable."
            )

