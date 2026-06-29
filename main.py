from app.chat import chat_with_ai

def main():
    print("AI助手启动，输入exit退出")

    while True:
        user_input = input("你：")

        if user_input == "exit":
            print("程序已退出")
            break

        reply = chat_with_ai(user_input)
        print("AI:", reply)


if __name__ == "__main__":
    main()

