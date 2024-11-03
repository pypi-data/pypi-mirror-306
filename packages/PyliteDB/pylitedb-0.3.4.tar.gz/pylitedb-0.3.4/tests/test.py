from src.Pylite import Database,email,password,Table

# db = Database("DataBase.pylite", "password",AutoSave=True)#.LoadFromSQL("test.db")
# # db.Users.afterInsert = lambda table,added: print("Inserted",added)
# # db.Users.Insert(ID = 1, Email = "ilies@gmail.com", Password = "passwordA1.")
# print(db.Users[0])



# db = Database()
# db.CreateTable("Users").AddColumn(
#     ID = int,
#     Email = email,
#     Password = password
# )
# db.Users.afterInsert = lambda table,added: print("Inserted",added.Email)
# db.Save("DataBase.pylite", "password")

db = Database("Database.pylite","SkillZone@2025")
print(db.Accounts.Columns)
db.Accounts.afterInsert = lambda table,added: print("Inserted",added)
db.Accounts.Insert(ID = 1, Email = "ilies@gmail.com", Password = "passwordA1.")
# db.CreateTable("Accounts").AddColumn(
#         ID=int,
#         Email=email,
#         Password=password,
#         Username=str,
#         Confirmed=bool,
#         Setup=bool,
#         JoinDate=str,
#         LastLogin=str,
#     )
# db.Save("Database.pylite","SkillZone@2025")
