var graf;
let etiquetas = document.getElementById('ejeX').innerHTML
let datos = document.getElementById('ejeY').innerHTML

function crearGrafico(t) {

    var tip = t;
    console.log(tip);
    console.log(datos);
    console.log(etiquetas);
    console.log(colores);

    switch (tip) {
        case "gen":
            genG();
            break;
        case "cat":
            cateG();
            break;
        case "ult":
            ultimosG();
            break;
        default:
            console.log("Opción inválida");
    }
}
function genG() {
    if (graf) {
        graf.destroy();
    }
    var conf = {
        labels: etiquetas,
        datasets: [
            {
                data: datos,
                backgroundColor: colores,
            },
        ],
    };

    var opciones = {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                display: false
            },
            datalabels: {
                display: false
            }
        }
    };

    var contexto = document.getElementById("grafico").getContext("2d");
    graf = new Chart(contexto, {
        type: "line",
        data: conf,
        options: opciones,
    });
}
function grafAct() {
    /* if (graf) {
        graf.destroy();
    } */
    console.log(etiquetas);
    console.log(datos);
/*     etiquetas = etiquetas.filter(label => label !== undefined);
    datos = datos.filter(dato => dato !== undefined); */
    var conf = {
        labels: [ 1, 2, 3, 4],
        datasets: [
            {
                data: [12, 24, 56, 78],
                //backgroundColor: colores,
            },
        ],
    };

    var opciones = {
        responsive: true,
        maintainAspectRatio: true // Desactivar el mantenimiento del aspecto de la relación de aspecto
    };

    var contexto = document.getElementById("grafico").getContext("2d");
    graf = new Chart(contexto, {
        type: "pie",
        data: conf,
        options: opciones,
    });
}
function ultimosG() {
    if (graf) {
        graf.destroy();
    }
    var conf = {
        labels: etiquetas,
        datasets: [
            {
                data: datos,
                backgroundColor: colores,
            },
        ],
    };

    var opciones = {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        plugins: {
            legend: {
                display: false
            }
        }
    };

    var contexto = document.getElementById("grafico").getContext("2d");
    graf = new Chart(contexto, {
        type: "bar",
        data: conf,
        options: opciones,
    });
}