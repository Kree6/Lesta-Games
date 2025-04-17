function updateFileName(input) {
    const fileName = input.files.length ? input.files[0].name : "Файл не выбран";
    document.getElementById("file-name").textContent = fileName;
}
