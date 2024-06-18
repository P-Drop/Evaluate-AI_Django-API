// Obtenemos el canvas y el contexto
const canvas = document.getElementById('canvasImg');
const ctx = canvas.getContext('2d');

// Variables para el dibujo y el JSON de coordenadas
let drawing = false;
let rect = {};
let rectangles = []; // Array para almacenar las coordenadas de los rectángulos dibujados
let id = 0;

// Función para dibujar un rectángulo
function drawRectangle(x, y, width, height) {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Limpiamos el canvas
    ctx.fillStyle = 'rgba(255, 128, 0, 0.3)'; // Color del relleno (rojo semi-transparente)
    ctx.strokeStyle = 'orange'; // Color del borde (rojo)

    // Dibujamos todos los rectángulos almacenados
    for (const rectangle of rectangles) {
        ctx.fillRect(rectangle.x, rectangle.y, rectangle.width, rectangle.height);
        ctx.strokeRect(rectangle.x, rectangle.y, rectangle.width, rectangle.height);
    }

    // Dibujamos el rectángulo actual
    ctx.fillRect(x, y, width, height);
    ctx.strokeRect(x, y, width, height);
}

// Función para capturar el inicio del dibujo del rectángulo
function handleMouseDown(event) {
    drawing = true;
    const { offsetX, offsetY } = event;
    rect.startX = offsetX;
    rect.startY = offsetY;
}

// Función para capturar el movimiento del ratón y actualizar el tamaño del rectángulo
function handleMouseMove(event) {
    if (!drawing) return;

    const { offsetX, offsetY } = event;
    rect.width = offsetX - rect.startX;
    rect.height = offsetY - rect.startY;

    // Redibujamos el canvas con todos los rectángulos almacenados y el rectángulo actual
    drawRectangle(rect.startX, rect.startY, rect.width, rect.height);
}

// Función para finalizar el dibujo del rectángulo
function handleMouseUp() {
    if (!drawing) return;
    drawing = false;
}

// Almacenamos el rectángulo en el array de coordenadas
function guardarEtiqueta(){    
    if (rect.width && rect.height) {
        rectangles.push({ id: id, x: rect.startX, y: rect.startY, width: rect.width, height: rect.height });
    }
    id = id + 1;
    document.getElementById('jsonNuevasEtiquetas').value = JSON.stringify(rectangles);
    document.getElementById("botonRevisar").type = "submit";
    console.log(JSON.stringify(rectangles));
}


// Agregamos los eventos al canvas
canvas.addEventListener('mousedown', handleMouseDown);
canvas.addEventListener('mousemove', handleMouseMove);
canvas.addEventListener('mouseup', handleMouseUp);

// Agregamos los eventos a los botones
const saveButton = document.getElementById('guardarEtiqueta');
saveButton.addEventListener('click', guardarEtiqueta);

