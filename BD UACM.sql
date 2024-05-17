create database uacm_2;
use uacm_2;

create table rol (
    id_rol int primary key,
    nombre_rol varchar (255) not null
);

create table persona (
    id_persona int primary key,
    id_rol int not null,
    nombre varchar(255) not null,
    apellido_m varchar (255) not null,
    apellido_p varchar (255) not null,
    telefono varchar (20) not null,
    correo varchar (255) not null,
    QR varchar (255) not null,
    contraseña varchar(255),
    foreign key (id_rol) references rol (id_rol)
);


create table reporte (
 id_reporte int primary key,
 id_persona int not null,
 tipo_reporte varchar (200) not null,
 fecha_reporte date,
 foreign key (id_persona) references persona (id_persona)
);

create table producto (
 id_producto int primary key,
 nombre_producto varchar (250) not null,
 cantidad int not null
);

create table inventario (
    id_inventario int primary key,
    id_producto int,
    fecha_inicio date not null,
    fecha_fin date not null,
    foreign key (id_producto) references producto (id_producto)
);

create table almacen (
 id_almacen int primary key,
 tipo_alamacen varchar (250) not null,
 dirección varchar (250),
 telefono int,
 correo varchar (250)
);

create table solicitud (
    id_solicitud int primary key,
    id_almacen int not null,
    id_persona int not null,
    fecha_solicitud date,
    cantidad int not null,
    foreign key (id_almacen) references almacen (id_almacen),
    foreign key (id_persona) references persona (id_persona)
);

create table reporte_producto (
    id_reporte int,
    id_producto int,
    cantidad_actual int not null,
    primary key (id_reporte, id_producto),
    foreign key (id_reporte) references reporte (id_reporte),
    foreign key (id_producto) references producto (id_producto)
);

create table persona_producto (
    id_persona int,
    id_producto int,
    tipo_transacción varchar (250),
    fecha date,
    primary key (id_persona, id_producto),
    foreign key (id_persona) references persona (id_persona),
    foreign key (id_producto) references producto (id_producto)
);


create table solicitud_producto (
    id_solicitud int,
    id_producto int,
    cantidad_producto int not null,
    primary key (id_solicitud, id_producto),
    foreign key (id_solicitud) references solicitud (id_solicitud),
    foreign key (id_producto) references producto (id_producto)
);

SELECT * FROM persona;
select * from almacen_app_producto;

call GenerarReporteProductos ('2024-04-09', '2024-05-15');
call Datos;
CALL Solicitud(1, 3, 2, 123, 101);

