from rest_framework import permissions

class isPerticipantOfConversation(permissions.BasePermission):
    """
    custom permission to allow only perticipants of a conversation
    to update, delete, add reaction within a conversation
    """

    def hasPermission(self, request, view):
        """
        Global permission to protect list view routes e.g GET /messages
        verify user is authenicated, first layer auth
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        read message object, ensure the message is read by its perticipant
        """

        if not (request.user and request.user.is_authenticated):
            return False
        
        #determine objected type
        conversation = None
        if hasattr(obj, 'conversation'): #check if object is a message obj
            conversation = obj.conversation
        if hasattr(obj, 'perticipants'): #check if object is a conversation object
            conversation = obj
        if not conversation:
            return False
        
        #validate request user is a perticipant of conversation
        is_perticipant = request.user in conversation.perticipants.all()

        if request.method in permissions.SAFE_METHODS: #check request method and grant perticipants access
            return is_perticipant 
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return is_perticipant
        elif request.method == 'POST':
            return is_perticipant
        
        return False




    