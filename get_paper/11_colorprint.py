print("字体色：")
s = '123456'


def log(info, level=0):
    if level == 0:
        print("\033[31m" + info + "\033[0m")
    elif level == 1:
        print("\033[34m" + info + "\033[0m")


print("\033[30m" + s + "\033[0m")
print("\033[31mSuixinBlog: https://suixinblog.cn\033[0m")
print("\033[32mSuixinBlog: https://suixinblog.cn\033[0m")
print("\033[4;33mSuixinBlog: https://suixinblog.cn \033[0m")
print("\033[34mSuixinBlog: https://suixinblog.cn\033[0m")
print("\033[1;35mSuixinBlog: https://suixinblog.cn\033[0m")
print("\033[4;36mSuixinBlog: https://suixinblog.cn\033[0m")
print("\033[37mSuixinBlog: https://suixinblog.cn\033[0m")
print("背景色：")
print("\033[1;37;40m\tSuixinBlog: https://suixinblog.cn\033[0m")
print("\033[37;41m\tSuixinBlog: https://suixinblog.cn\033[0m")
print("\033[37;42m\tSuixinBlog: https://suixinblog.cn\033[0m")
print("\033[37;43m\tSuixinBlog: https://suixinblog.cn\033[0m")
print("\033[37;44m\tSuixinBlog: https://suixinblog.cn\033[0m")
print("\033[37;45m\tSuixinBlog: https://suixinblog.cn\033[0m")
print("\033[37;46m\tSuixinBlog: https://suixinblog.cn\033[0m")
print("\033[1;30;47m\tSuixinBlog: https://suixinblog.cn\033[0m")
