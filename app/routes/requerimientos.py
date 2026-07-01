from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Requerimiento, Proyecto

bp_reqs = Blueprint('requerimientos', __name__)

CATEGORIAS_NF = ['rendimiento', 'seguridad', 'usabilidad', 'confiabilidad', 'mantenibilidad', 'escalabilidad', 'otro']

@bp_reqs.route('/')
def lista():
    proyecto_id = request.args.get('proyecto_id', type=int)
    proyectos = Proyecto.query.order_by(Proyecto.nombre).all()
    query = Requerimiento.query
    if proyecto_id:
        query = query.filter_by(proyecto_id=proyecto_id)
    reqs = query.order_by(Requerimiento.identificador).all()
    return render_template('requerimientos/lista.html', reqs=reqs, proyectos=proyectos, proyecto_id=proyecto_id)

@bp_reqs.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    proyectos = Proyecto.query.order_by(Proyecto.nombre).all()
    proyecto_id = request.args.get('proyecto_id', type=int)
    if request.method == 'POST':
        proyecto_id = request.form.get('proyecto_id', type=int)
        identificador = request.form.get('identificador', '').strip().upper()
        tipo = request.form.get('tipo', '')
        descripcion = request.form.get('descripcion', '').strip()
        prioridad = request.form.get('prioridad', 'media')
        estado = request.form.get('estado', 'pendiente')
        categoria = request.form.get('categoria') if tipo == 'no_funcional' else None
        if not proyecto_id or not identificador or not descripcion or tipo not in ('funcional', 'no_funcional'):
            flash('Todos los campos obligatorios deben completarse.', 'danger')
            return render_template('requerimientos/nuevo.html', proyectos=proyectos,
                                   proyecto_id=proyecto_id, categorias=CATEGORIAS_NF)
        if Requerimiento.query.filter_by(proyecto_id=proyecto_id, identificador=identificador).first():
            flash(f'Ya existe el identificador {identificador} en este proyecto.', 'danger')
            return render_template('requerimientos/nuevo.html', proyectos=proyectos,
                                   proyecto_id=proyecto_id, categorias=CATEGORIAS_NF)
        req = Requerimiento(proyecto_id=proyecto_id, identificador=identificador, tipo=tipo,
                            descripcion=descripcion, prioridad=prioridad, estado=estado, categoria=categoria)
        db.session.add(req)
        db.session.commit()
        flash(f'Requerimiento {identificador} creado.', 'success')
        return redirect(url_for('requerimientos.detalle', id=req.id))
    return render_template('requerimientos/nuevo.html', proyectos=proyectos,
                           proyecto_id=proyecto_id, categorias=CATEGORIAS_NF)

@bp_reqs.route('/<int:id>')
def detalle(id):
    req = Requerimiento.query.get_or_404(id)
    return render_template('requerimientos/detalle.html', req=req)

@bp_reqs.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    req = Requerimiento.query.get_or_404(id)
    proyectos = Proyecto.query.all()
    if request.method == 'POST':
        req.identificador = request.form.get('identificador', '').strip().upper()
        req.tipo = request.form.get('tipo', '')
        req.descripcion = request.form.get('descripcion', '').strip()
        req.prioridad = request.form.get('prioridad', '')
        req.estado = request.form.get('estado', '')
        req.categoria = request.form.get('categoria') if req.tipo == 'no_funcional' else None
        db.session.commit()
        flash('Requerimiento actualizado.', 'success')
        return redirect(url_for('requerimientos.detalle', id=id))
    return render_template('requerimientos/editar.html', req=req, proyectos=proyectos, categorias=CATEGORIAS_NF)

@bp_reqs.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    req = Requerimiento.query.get_or_404(id)
    proyecto_id = req.proyecto_id
    ident = req.identificador
    db.session.delete(req)
    db.session.commit()
    flash(f'Requerimiento {ident} eliminado.', 'info')
    return redirect(url_for('proyectos.detalle', id=proyecto_id))