from typing import Optional

from app.company import CompanyPool, Company


__all__ = [
    'extract_account_id',
    'get_company_from_context'
]


def extract_account_id(context) -> Optional[str]:
    for key, value in context.invocation_metadata():
        if key == 'account-id':
            return value
    else:
        return None


async def get_company_from_context(company_pool: CompanyPool, context) -> Company:
    account_id = extract_account_id(context)

    return await company_pool.get(account_id)
