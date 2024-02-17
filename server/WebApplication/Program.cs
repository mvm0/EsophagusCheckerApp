using System.Diagnostics;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddCors();
var app = builder.Build();
app.UseCors(builder => builder.AllowAnyOrigin());

app.Run(async (context) =>
{
    var request = context.Request;
    var path = context.Request.Path;
    Console.WriteLine($"Request received: {request.Method}");
    if (request.Method == "GET")
    {
        context.Response.Headers["Content-Type"] = "images; charset=utf-8";
        var fullPath = $"images/{path}";
        await context.Response.SendFileAsync($"{fullPath}");
        Console.WriteLine($"File sent to client: images/{path}");
    }
    else if (request.Path == "/upload" && request.Method == "POST")
    {
        IFormFileCollection files = request.Form.Files;
        var newFileName = Transliteration.Translit(files[0].FileName.Replace(" ", ""));
        var uploadPath = $"images/{newFileName}";
        using (var fileStream = new FileStream(uploadPath, FileMode.Create))
        {
            await files[0].CopyToAsync(fileStream);
        }
        Console.WriteLine($"Uploaded custom image: {newFileName}");

        ProcessStartInfo start = new ProcessStartInfo();
        start.FileName = "NN/.venv/Scripts/python.exe";
        start.Arguments = string.Format("{0} {1}", "NN/main.py", $"\"images/{newFileName}\"");
        start.RedirectStandardOutput = true;
        string result = "";
        using (Process process = Process.Start(start))
        {
            using (StreamReader reader = process.StandardOutput)
            {
                result = reader.ReadToEnd();
            }
        }
        string[] links = result.Replace("\r\n", "").Split("%");

        NewImagesJSON imageJSON = new($"{links[0]}", $"{links[1]}", $"{links[2]}", $"{links[3]}");
        await context.Response.WriteAsJsonAsync(imageJSON);
        Console.WriteLine($"JSON sent to client: {imageJSON}");

        string[] allFiles = Directory.GetFiles("images/");
        foreach (string file in allFiles)
        {
            if (DateTime.Now - File.GetLastWriteTime(file) > TimeSpan.FromMinutes(30))
            {
                Console.WriteLine($"Deleted file (exists for more than 30 minutes): {file}");
                File.Delete(file);
            }
        }
    }
});

app.Run();

public record NewImagesJSON(string originalImage, string newImage1, string newImage2, string newImage3);