formElem.onsubmit = async (e) => {
    e.preventDefault();

    let response = await fetch('http://localhost:5077/upload', {
      method: 'POST',
      body: new FormData(formElem)
    });
    let tmpRes = await response.text();
    let images = [
        JSON.parse(tmpRes).originalImage,
        JSON.parse(tmpRes).newImage1,
        JSON.parse(tmpRes).newImage2,
        JSON.parse(tmpRes).newImage3
    ];
    for(let i = 0; i < 4; i++) {
        let img = document.createElement("img");
        img.src = `http://localhost:5077/${images[i]}`;
        let src = document.getElementById("header");
        src.appendChild(img);
    }
  };