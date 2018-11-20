from api.context import Context

context = Context("", "", "", "")

user = context.create_user("cisjbutt", "jack", "butterworth", "jackdavidbutterworth@gmail.com", "1986-02-28")

users = context.get_users()
for user in users:
    print(user.forename)
