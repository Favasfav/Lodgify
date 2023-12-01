# from rest_framework import permissions
# from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
class Userpermission(BasePermission):

    def has_permission(self, request,view):
      print("hhjhjh")
      print("uuuuuuuuuuuuu",request.user)
      if request.user.is_authenticated: 
            print("authenticated")
            if request.user.role=="user":
                return True
            return False
      print("nouser")
      return False
     
class Partnerpermission(BasePermission):

    

    def has_permission(self, request, view):
        if request.user.role=="partner":
            return True
        return False    
    

class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False       