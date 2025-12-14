from django.shortcuts import render, redirect
import subprocess
from .models import SharedCode

def cpp(request):
    cpp_output = None
    cpp_code = request.session.get("cpp_code", "")
    cpp_input_data= request.session.get("cpp_input", "")

    if request.method == "POST":
        cpp_code = request.POST.get("cpp_code", "")
        cpp_input_data = request.POST.get("cpp_input", "")
        language = "cpp"
        
        # print("inside block of post req :")
        # print( cpp_code)
        # print("Did you see the message")

        request.session["cpp_code"] = cpp_code
        request.session["cpp_input"] = cpp_input_data

        if request.POST.get("action") == "share":
            shared = SharedCode.objects.create(
                language=language,
                code=cpp_code,
                input_data=cpp_input_data
            )
            print("hi", shared.unique_id)
            return redirect(f"/share/{shared.unique_id}")
             
        if language == "cpp":
            with open("temp2.cpp", "w") as file:
                file.write(cpp_code)
        try:
            compile_process = subprocess.run(
                ["g++", "temp2.cpp", "-o", "temp2.out"], capture_output=True, text=True
            )

            if compile_process.returncode != 0:
                cpp_output = compile_process.stderr
            else:
                run_process = subprocess.run(
                    ["./temp2.out"],
                    input=cpp_input_data,
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                cpp_output = run_process.stdout

        except subprocess.TimeoutExpired:
            cpp_output = "Time Limit Exceeded"
        except Exception as e:
            cpp_output = str(e)

    return render(request, "cpp.html", {"cpp_code": cpp_code, "cpp_input_data": cpp_input_data, "cpp_output": cpp_output})

def java(request):
    java_output = None
    java_code = request.session.get("java_code", "")
    java_input_data= request.session.get("java_input", "")

    if request.method == "POST":
        java_code = request.POST.get("java_code", "")
        java_input_data = request.POST.get("java_input", "")
        language = "java"
        
        # print("inside block of post req :")
        # print( java_code)
        # print("Did you see the message")

        request.session["java_code"] = java_code
        request.session["java_input"] = java_input_data

        if language == "java":
            with open("Main.java", "w") as file:
                file.write(java_code)
        try:
            compile_process = subprocess.run(
                ["javac", "Main.java"], capture_output=True, text=True
            )

            if compile_process.returncode != 0:
                java_output = compile_process.stderr
            else:
                run_process = subprocess.run(
                    ["java", "Main"],
                    input=java_input_data,
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                java_output = run_process.stdout

        except subprocess.TimeoutExpired:
            java_output = "Time Limit Exceeded"
        except Exception as e:
            java_output = str(e)

    return render(request, "java.html", {"java_code": java_code, "java_input_data": java_input_data, "java_output": java_output})

def home(request):
    output = None
    code = request.session.get("code", "")  
    input_data = request.session.get("input", "")   

    if request.method == "POST":
        code = request.POST.get("code")
        input_data = request.POST.get("input")
        language = "python"

        request.session["code"] = code
        request.session["input"] = input_data

        if language == "python":
            with open("temp.py", "w") as file:
                file.write(code)
            try:
                process = subprocess.run(
                    ["python", "temp.py"],
                    input=input_data,
                    text=True,
                    capture_output=True,
                    timeout=5
                )
                output = process.stdout if process.returncode == 0 else process.stderr
            except subprocess.TimeoutExpired:
                output = "Time Limit Exceeded"
            except Exception as e:
                output = str(e) 
    return render(request, "index.html", {"output": output, "code": code, "input_data": input_data})


def cpp_compiler(request):
    if request.method == "POST":
        code = request.POST.get("code")
        language = request.POST.get("language")
        input_data = request.POST.get("cpp_input")

        # If user clicks Share
        if request.POST.get("action") == "share":
            shared = SharedCode.objects.create(
                language=language,
                code=code,
                input_data=input_data
            )
            print("hi", shared.unique_id)
            return redirect(f"/share/{shared.unique_id}")
        

def view_shared_code(request, uid):
    print(uid)
    shared = SharedCode.objects.get(unique_id=uid)
    return render(request, "cpp.html", {
        "cpp_code": shared.code,
        "cpp_input_data": shared.input_data,
        "cpp_output" : None
    })