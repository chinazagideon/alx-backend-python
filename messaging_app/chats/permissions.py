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
        
        if isinstance(obj, type(view.queryset.model)): 
            return request.user in obj.conversation.all()
        

        elif isinstance(obj, type(view.setmodal.modal)):
            return request.user in obj,isPerticipantOfConversation 
        
        return False



    