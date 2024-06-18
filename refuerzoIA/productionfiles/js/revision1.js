const canvas = document.getElementById('canvasImg');
const ctx = canvas.getContext('2d');
var jsonString = document.getElementById('jsonInf').innerText
var datosImagen = JSON.parse(jsonString);
document.getElementById("datosImagen").value = JSON.stringify(datosImagen);
    
// Accede a la lista de objetos dentro del JSON
var rectangles = datosImagen.label_stats;
    
// Recorre la lista de objetos y los dibuja en el canvas
rectangles.forEach(rectangle => {
  ctx.lineWidth = 2;
  ctx.strokeStyle = rectangle.color;
  ctx.strokeRect(rectangle.col_min, rectangle.row_min, rectangle.col_inc, rectangle.row_inc);
});

// Agregar eventos de clic para cambiar el color del rectángulo
canvas.addEventListener("click", function(event) {
    const rect = canvas.getBoundingClientRect();
    const mouseX = (event.clientX - rect.left)*900/rect.width;
    const mouseY = (event.clientY - rect.top)*900/rect.height;

    rectangles.forEach(rectangle => {
      if (
        mouseX >= rectangle.col_min &&
        mouseX <= rectangle.col_min + rectangle.col_inc &&
        mouseY >= rectangle.row_min &&
        mouseY <= rectangle.row_min + rectangle.row_inc
      ) {
        // Cambiar el color del rectángulo al hacer clic
        rectangle = getColor(rectangle);

        // Volver a dibujar todos los rectángulos en el canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        rectangles.forEach(rectan => {
          ctx.strokeStyle = rectan.color;
          if(rectan.color == "red" || rectan.color == "green"){ctx.lineWidth = 6;}
          else{ctx.lineWidth = 2;}          
          ctx.strokeRect(rectan.col_min, rectan.row_min, rectan.col_inc, rectan.row_inc);
        });
      }
    });
    document.getElementById("botonRevisar").type = "submit";
    document.getElementById("datosImagen").value = JSON.stringify(datosImagen);
    
  });

  // Función auxiliar para cambiar de color el rectángulo
function getColor(r) {
    switch (r.color) {
      case "purple":
          r.color = "green";
          r.state = "ok";
        break;

      case "green":
          r.color = "red";
          r.state = "error";
        break;

      case "red":
          r.color = "purple";
          r.state = "default";
        break;
    
      default:
        break;
    }
    return r;
  }