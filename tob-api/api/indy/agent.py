import asyncio

from von_agent.nodepool import NodePool
from von_agent.demo_agents import OrgBookAgent


class Agent:

    # Singleton
    class __Agent:

        async def start():
            global pool
            global orgbook

            print('connecting to node pool with genesis txn file:')
            print('/opt/app-root/genesis')

            pool = NodePool(
                # Hack to use different pool names. Agent lib doesn't support
                # reopening existing pool config...
                'theorgbook',
                '/opt/app-root/genesis')
            await pool.open()
            orgbook = OrgBookAgent(
                pool,
                'The-Org-Book-Agent-0000000000000',
                'the-org-book-agent-wallet',
                None,
                '127.0.0.1',
                9702,
                'api/v0')
            await orgbook.open()
            await orgbook.create_master_secret('secret')

    instance = None

    def __init__(self, arg):
        if not Agent.instance:
            Agent.instance = Agent.__Agent(arg)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(Agent.instance.start())
            loop.close()

    def __getattr__(self, name):
        return getattr(self.instance, name)
