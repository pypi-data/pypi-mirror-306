
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from eis.accounting.api.booking_processes_api import BookingProcessesApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from eis.accounting.api.booking_processes_api import BookingProcessesApi
from eis.accounting.api.financial_accounts_api import FinancialAccountsApi
from eis.accounting.api.health_api import HealthApi
