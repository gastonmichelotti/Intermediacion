

    with PreciosZonas as (
    select 
    u.id as idUsuario,
    u.alias,
    u.idzona, 
    case when u.idzona in (258, 248, 247, 242, 241, 229, 224, 217, 216, 211, 209, 208, 207, 206, 189, 167, 228, 230) then 1 else 0 end as EsGBA,
    z.nombre,
    p.id as idprecio,
    pr.id as idprogramacion,
    case when pr.id is not null then p.PrecioMotoboyHora4SemanaDia + pr.PrecioMotoboyHora4SemanaDia else p.PrecioMotoboyHora4SemanaDia end as PrecioMotoboyHoraSemanaDiaZona,
    case when pr.id is not null then p.PrecioMotoboyHora4FindeDia + pr.PrecioMotoboyHora4FindeDia else p.PrecioMotoboyHora4FindeDia end as PrecioMotoboyHoraFindeDiaZona,
    case when pr.id is not null then p.PrecioMotoboyHora3SemanaNoche + pr.PrecioMotoboyHora3SemanaNoche else p.PrecioMotoboyHora3SemanaNoche end as PrecioMotoboyHora3SemanaNocheZona,
    case when pr.id is not null then p.PrecioMotoboyHora4SemanaNoche + pr.PrecioMotoboyHora4SemanaNoche else p.PrecioMotoboyHora4SemanaNoche end as PrecioMotoboyHora4SemanaNocheZona,
    case when pr.id is not null then p.PrecioMotoboyHora5SemanaNoche + pr.PrecioMotoboyHora5SemanaNoche else p.PrecioMotoboyHora5SemanaNoche end as PrecioMotoboyHora5SemanaNocheZona,
    case when pr.id is not null then p.PrecioMotoboyHora6SemanaNoche + pr.PrecioMotoboyHora6SemanaNoche else p.PrecioMotoboyHora6SemanaNoche end as PrecioMotoboyHora6SemanaNocheZona,
    case when pr.id is not null then p.PrecioMotoboyHora3FindeNoche + pr.PrecioMotoboyHora3FindeNoche else p.PrecioMotoboyHora3FindeNoche end as PrecioMotoboyHora3FindeNocheZona,
    case when pr.id is not null then p.PrecioMotoboyHora4FindeNoche + pr.PrecioMotoboyHora4FindeNoche else p.PrecioMotoboyHora4FindeNoche end as PrecioMotoboyHora4FindeNocheZona,
    case when pr.id is not null then p.PrecioMotoboyHora5FindeNoche + pr.PrecioMotoboyHora5FindeNoche else p.PrecioMotoboyHora5FindeNoche end as PrecioMotoboyHora5FindeNocheZona,
    case when pr.id is not null then p.PrecioMotoboyHora6FindeNoche + pr.PrecioMotoboyHora6FindeNoche else p.PrecioMotoboyHora6FindeNoche end as PrecioMotoboyHora6FindeNocheZona
    from usuario u with (nolock)
    inner join zona z with (nolock) on u.idzona = z.id
    inner join precio p with (nolock) on z.idprecio = p.id
    left join programacion pr with (nolock) on p.id = pr.idprecio and pr.FechaProgramacion >= GETDATE()
    where u.id in (20307, 30984, 21626, 26274, 14264, 28888)
    )
    , 
    -- select * from PreciosZonas
    reservas as (
    select 
    u.id as idUsuario, 
    isnull(sum(case when DATEPART(weekday, r.fecha) in (2,3,4,5) and r.esmañana = 1 and datediff(hour, r.fechaDesde, r.fechaHasta) < 4 then datediff(minute, r.fechaDesde, r.fechaHasta)/60.00 end), 0) as QHora3SemanaDia,
    isnull(sum(case when DATEPART(weekday, r.fecha) in (2,3,4,5) and r.esmañana = 1 and datediff(hour, r.fechaDesde, r.fechaHasta) >= 4 then datediff(minute, r.fechaDesde, r.fechaHasta)/60.00 end), 0) as QHora4SemanaDia,
    isnull(sum(case when DATEPART(weekday, r.fecha) in (1,6) and r.esmañana = 1 and datediff(hour, r.fechaDesde, r.fechaHasta) < 4 then datediff(minute, r.fechaDesde, r.fechaHasta)/60.00 end), 0) as QHora3FindeDia,
    isnull(sum(case when DATEPART(weekday, r.fecha) in (1,6) and r.esmañana = 1 and datediff(hour, r.fechaDesde, r.fechaHasta) >= 4 then datediff(minute, r.fechaDesde, r.fechaHasta)/60.00 end), 0) as QHora4FindeDia,
    isnull(sum(case when DATEPART(weekday, r.fecha) in (2,3,4,5) and r.esmañana = 0 and datediff(hour, r.fechaDesde, r.fechaHasta) < 4 then datediff(minute, r.fechaDesde, r.fechaHasta)/60.00 end), 0) as QHora3SemanaNoche,
    isnull(sum(case when DATEPART(weekday, r.fecha) in (2,3,4,5) and r.esmañana = 0 and datediff(hour, r.fechaDesde, r.fechaHasta) = 4 then datediff(minute, r.fechaDesde, r.fechaHasta)/60.00 end), 0) as QHora4SemanaNoche,
    isnull(sum(case when DATEPART(weekday, r.fecha) in (2,3,4,5) and r.esmañana = 0 and datediff(hour, r.fechaDesde, r.fechaHasta) = 5 then datediff(minute, r.fechaDesde, r.fechaHasta)/60.00 end), 0) as QHora5SemanaNoche,
    isnull(sum(case when DATEPART(weekday, r.fecha) in (2,3,4,5) and r.esmañana = 0 and datediff(hour, r.fechaDesde, r.fechaHasta) >= 6 then datediff(minute, r.fechaDesde, r.fechaHasta)/60.00 end), 0) as QHora6SemanaNoche,
    isnull(sum(case when DATEPART(weekday, r.fecha) in (1,6) and r.esmañana = 0 and datediff(hour, r.fechaDesde, r.fechaHasta) < 4 then datediff(minute, r.fechaDesde, r.fechaHasta)/60.00 end), 0) as QHora3FindeNoche,
    isnull(sum(case when DATEPART(weekday, r.fecha) in (1,6) and r.esmañana = 0 and datediff(hour, r.fechaDesde, r.fechaHasta) = 4 then datediff(minute, r.fechaDesde, r.fechaHasta)/60.00 end), 0) as QHora4FindeNoche,
    isnull(sum(case when DATEPART(weekday, r.fecha) in (1,6) and r.esmañana = 0 and datediff(hour, r.fechaDesde, r.fechaHasta) = 5 then datediff(minute, r.fechaDesde, r.fechaHasta)/60.00 end), 0) as QHora5FindeNoche,
    isnull(sum(case when DATEPART(weekday, r.fecha) in (1,6) and r.esmañana = 0 and datediff(hour, r.fechaDesde, r.fechaHasta) >= 6 then datediff(minute, r.fechaDesde, r.fechaHasta)/60.00 end), 0) as QHora6FindeNoche
    from ReservaxMotoboy r with (nolock)
    inner join usuario u with (nolock) on r.idusuario = u.id
    where 
    (r.cancelada = 0 or (r.cancelada = 1 and r.IdMotivoCancelada = 5))
    and r.fecha >= DATEADD(WEEK, -4, DATEADD(WEEK, DATEDIFF(WEEK, 0, GETDATE()), 0))
    and u.id in (20307, 30984, 21626, 26274, 14264, 28888)
    group by u.id
    )
    select 
    PreciosZonas.*,
    reservas.QHora3SemanaDia,
    reservas.QHora4SemanaDia,
    reservas.QHora3FindeDia,
    reservas.QHora4FindeDia,
    reservas.QHora3SemanaNoche,
    reservas.QHora4SemanaNoche,
    reservas.QHora5SemanaNoche,
    reservas.QHora6SemanaNoche,
    reservas.QHora3FindeNoche,
    reservas.QHora4FindeNoche,
    reservas.QHora5FindeNoche,
    reservas.QHora6FindeNoche
    from PreciosZonas
    inner join reservas on PreciosZonas.idUsuario = reservas.idUsuario

