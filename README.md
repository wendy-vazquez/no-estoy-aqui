# Informacion personal de los creadores
### Integrante 1:
- **Nombre**: Vazquez Ortiz Wendy Judith
- **Edad**: 17
- **Grado y grupo**: 6D
- **Numero de control**: 23308060610440
- **Correo Electronico**: 23308060610440@cetis61.edu.mx
- **Foto**:<img width="150" height="200" alt="awua" src="https://github.com/user-attachments/assets/90318cc7-d603-4e7d-bc99-4add8723d4e9" />

### Integrante 2:
- **Nombre**: Jaime Alberto Espinoza Martínez
- **Edad**: 17
- **Grado y grupo**: 6D
- **Numero de control**: 23308060610540
- **Correo Electronico**: 23308060610540@cetis61.edu.mx
- **Foto**: <img width="200" height="220" alt="bebeto" src="https://github.com/user-attachments/assets/8a4dca21-bc63-46c8-8504-515aaff666e0" />


# Propósito del proyecto

El proyecto **“No estoy aquí”** tiene como propósito desarrollar una aplicación interactiva con enfoque narrativo y psicológico, utilizando Python y el framework Flet, que permita al usuario explorar diferentes escenarios relacionados con sueños, recuerdos y la percepción de la identidad. La aplicación busca ofrecer una experiencia inmersiva mediante la interacción con distintas escenas, diálogos y decisiones que afectan el desarrollo de la historia.

Además del aspecto visual y narrativo, el proyecto tiene como finalidad aplicar conocimientos de programación orientada a objetos, arquitectura MVC y gestión de bases de datos relacionales, integrando un sistema de usuarios y almacenamiento de progreso mediante MySQL.

---

# Alcance del proyecto

El alcance del proyecto contempla el desarrollo de un prototipo funcional de videojuego narrativo que permita:

- Registrar e iniciar sesión de usuarios.
- Guardar el progreso de cada jugador.
- Gestionar escenas y transiciones dentro del juego.
- Registrar decisiones tomadas por el usuario.
- Implementar un sistema de emociones y variables psicológicas.
- Mostrar diferentes finales dependiendo de las decisiones realizadas.
- Aplicar una interfaz gráfica interactiva y estética utilizando Flet.

El sistema contará con una estructura organizada bajo el patrón MVC (Modelo-Vista-Controlador), permitiendo separar la lógica de negocio, las vistas y el acceso a datos para facilitar el mantenimiento y la escalabilidad del proyecto.

## No se contempla en esta etapa:

- Multijugador en línea.
- Sincronización en la nube.
- Motor gráfico 3D.
- Inteligencia artificial avanzada.
- Compatibilidad móvil nativa.

---

# Entidades que intervienen en el flujo de información

## Usuario

Entidad encargada de almacenar la información principal del jugador:

- Nombre de usuario.
- Correo electrónico.
- Contraseña.
- Fecha de creación.

Un usuario puede tener múltiples registros relacionados con progreso, decisiones y finales obtenidos.

---

## Progreso del juego

Almacena el estado actual de la partida del usuario:

- Escena actual.
- Nivel de miedo.
- Nivel de nostalgia.
- Identidad.
- Curiosidad.
- Estado del espejo.
- Fecha de guardado.

Permite continuar la partida desde el último punto registrado.

---

## Decisiones

Registra las elecciones realizadas por el jugador durante la narrativa.

Cada decisión puede influir en:

- Diálogos.
- Escenas.
- Emociones.
- Finales desbloqueados.

---

## Sueños

Contiene información relacionada con los sueños o recuerdos desbloqueados durante el juego.

Permite almacenar:

- Nombre del sueño.
- Descripción.
- Fecha de descubrimiento.

---

## Finales

Entidad destinada a almacenar los finales obtenidos por el jugador dependiendo de sus acciones dentro de la historia.

---

## Configuración

Guarda preferencias personalizadas del usuario, por ejemplo:

- Volumen.
- Velocidad de texto.
- Activación de efectos visuales.

---

# Diseño del diagrama ER

El modelo entidad-relación (ER) fue diseñado considerando principios de normalización para evitar redundancia de datos y mantener la integridad de la información.

La estructura se encuentra normalizada principalmente hasta la tercera forma normal (3FN), ya que:

- Cada tabla contiene información específica.
- No existen dependencias parciales.
- Se evita la duplicación innecesaria de datos.
- Las relaciones entre entidades se realizan mediante claves foráneas.

## Relaciones principales

- Un usuario puede tener un progreso de juego.
- Un usuario puede registrar múltiples decisiones.
- Un usuario puede desbloquear múltiples sueños.
- Un usuario puede obtener múltiples finales.
- Un usuario posee una configuración personalizada.

---

# Desarrollo de la base de datos

La base de datos será desarrollada en MySQL Workbench utilizando tablas relacionadas mediante claves primarias y claves foráneas.

Se implementarán restricciones de integridad referencial para garantizar:

- Consistencia de los datos.
- Correcta relación entre entidades.
- Prevención de registros huérfanos.

Asimismo, se validarán:

- Unicidad de usuarios y correos electrónicos.
- Obligatoriedad de campos esenciales.
- Relaciones correctas entre tablas.

# Etapas de entrega del proyecto

## Etapa 1:
Registro e inicio de sesion para los usuarios.
## Etapa 2:
Recuperacion de contraseña/ cambio de contraseña
## Etapa 3:
Perfil del usuario,