
class ChatService:
    def __init__(self,conn):
        self.conn = conn
        
    async def SendMessage(self,request):
       return await self.conn.getResponse(request.message)
    
    async def search(self,request):
        return await self.conn.search(request.message)
