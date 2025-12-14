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

    return render(request, "cpp.html", {"cpp_code": cpp_code, "cpp_input_data": cpp_input_data.rstrip(), "cpp_output": cpp_output})


def c(request):
    c_output = None
    c_code = request.session.get("c_code", "")
    c_input_data= request.session.get("c_input", "")

    if request.method == "POST":
        c_code = request.POST.get("c_code", "")
        c_input_data = request.POST.get("c_input", "")
        language = "c"
        
        request.session["c_code"] = c_code
        request.session["c_input"] = c_input_data

        if request.POST.get("action") == "share":
            shared = SharedCode.objects.create(
                language=language,
                code=c_code,
                input_data=c_input_data
            )
            print("hi", shared.unique_id)
            return redirect(f"/share/{shared.unique_id}")
             
        if language == "c":
            with open("tempc.c", "w") as file:
                file.write(c_code)
        try:
            compile_process = subprocess.run(
                ["gcc", "tempc.c", "-o", "tempc"], capture_output=True, text=True
            )

            if compile_process.returncode != 0:
                c_output = compile_process.stderr
            else:
                run_process = subprocess.run(
                    ["./tempc"],
                    input=c_input_data,
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                c_output = run_process.stdout

        except subprocess.TimeoutExpired:
            c_output = "Time Limit Exceeded"
        except Exception as e:
            c_output = str(e)

    return render(request, "c_lang.html", {"c_code": c_code, "c_input_data": c_input_data.rstrip(), "c_output": c_output})

def java(request):
    java_output = None
    java_code = request.session.get("java_code", "")
    java_input_data= request.session.get("java_input", "")

    if request.method == "POST":
        
        java_code = request.POST.get("java_code", "")
        print(len(java_code))
        java_input_data = request.POST.get("java_input", "")
        language = "java"
        
        request.session["java_code"] = java_code
        request.session["java_input"] = java_input_data

        if request.POST.get("action") == "share":
            shared = SharedCode.objects.create(
                language=language,
                code=java_code,
                input_data=java_input_data
            )
            print("hi java here", shared.unique_id)
            return redirect(f"/share/{shared.unique_id}")

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

    return render(request, "java.html", {"java_code": java_code, "java_input_data": java_input_data.rstrip(), "java_output": java_output})

def home(request):
    py_output = None
    py_code = request.session.get("py_code", "")  
    py_input_data = request.session.get("py_input", "")   

    if request.method == "POST":
        
        py_code = request.POST.get("py_code","")
        py_input_data = request.POST.get("py_input", "")
        language = "python"

        request.session["code"] = py_code
        request.session["input"] = py_input_data

        if request.POST.get("action") == "share":
            shared = SharedCode.objects.create(
                language=language,
                code=py_code,
                input_data=py_input_data
            )
            print("hi python here", shared.unique_id)
            return redirect(f"/share/{shared.unique_id}")

        if language == "python":
            with open("temp.py", "w") as file:
                file.write(py_code)
            try:
                process = subprocess.run(
                    ["python", "temp.py"],
                    input=py_input_data,
                    text=True,
                    capture_output=True,
                    timeout=5
                )
                py_output = process.stdout if process.returncode == 0 else process.stderr
                
            except subprocess.TimeoutExpired:
                py_output = "Time Limit Exceeded"
            except Exception as e:
                py_output = str(e) 
    return render(request, "index.html", {"py_output": py_output, "py_code": py_code, "input_data": py_input_data.rstrip()})

   
def view_shared_code(request, uid):
    print(uid)
    shared = SharedCode.objects.get(unique_id=uid)
    language = shared.language

    if(language=='cpp'): 
        return render(request, "cpp.html", {
            "cpp_code": shared.code,
            "cpp_input_data": shared.input_data,
            "cpp_output" : None
        })
    if(language=='java'): 
        return render(request, "java.html", {
            "java_code": shared.code,
            "java_input_data": shared.input_data,
            "java_output" : None
        })
    if(language=='c'): 
        return render(request, "c_lang.html", {
            "c_code": shared.code,
            "c_input_data": shared.input_data,
            "c_output" : None
        })
    if(language=='python'): 
        return render(request, "index.html", {
            "py_code": shared.code,
            "py_input_data": shared.input_data,
            "py_output" : None
        })