from django.db import models
from django.conf import settings
from django.db import transaction

class FriendList(models.Model):

	user 				= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
	friends 			= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends") 


	def __str__(self):
		return self.user.username

	def add_friend(self, account):
		"""
		Add a new friend.
		"""
		if account not in self.friends.all():
			self.friends.add(account)
			self.save()


	def remove_friend(self, account):
		"""
		Remove a friend.
		"""
		if account in self.friends.all():
			self.friends.remove(account)
			
	def unfriend(self, removee):
		"""
		Initiate the action of unfriend. remove both from each others friend list.
		"""
		# The person terminating friendship.
		remover_friend_list = self 
		# Removing the friend from friendlist.
		remover_friend_list.remove_friend(removee)

		# Removee friendlist
		removee_friend_list = FriendList.objects.get(user=removee)
		# Removing himself from removee friendlist
		removee_friend_list.remove_friend(self.user)
		
	def is_mutual_friend(self, friend):
		try:
			friend_list = FriendList.objects.get(user=friend)
			return self.user in friend_list.friends.all() and friend in self.friends.all()
		except FriendList.DoesNotExist:
			return False


class FriendRequest(models.Model):
	"""
	It consists two important parts.
		1. SENDER: who send request
		2. RECEIVER: who receive the request.
	"""
	sender 			= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
	receiver 		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
	is_active 		= models.BooleanField(blank=True, null=False, default=True)		
	timestamp		= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.username
	

	def accept(self):
		"""
		Accept friend request.
		Update both SENDER and RECEIVER friendlist
		"""

		if not self.is_active:
			raise ValueError("This friend request is already inactive.")
		with transaction.atomic():
			try:
				receiver_friend_list, _ = FriendList.objects.get_or_create(user = self.receiver)
				sender_friend_list, _ 	= FriendList.objects.get_or_create(user = self.sender)
				
				if receiver_friend_list:
					receiver_friend_list.add_friend(self.sender)
				if sender_friend_list:
					sender_friend_list.add_friend(self.receiver)

					self.is_active = False
					self.save()

			except Exception as e:
				raise RuntimeError(f"An error occureed while accepting a friend request: {e}")
	def decline(self):
		"""
		Decline a friend request.
		It is 'Declined by a setting 'is_active' field to False. --Done by receiver
		"""
		self.is_active = False
		self.save()
	
	def cancel(self):
		"""
		Cancel a friend request.
		It is 'Canceld' by a setting 'is_active' field to False. --Done by sender.
		The only different with respect to "declining" through the notification that is generated. 
		"""
		self.is_active = False
		self.save()
