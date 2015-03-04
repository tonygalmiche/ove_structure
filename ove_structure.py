# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
import time

from openerp.osv import fields
from openerp.osv import osv
from openerp.tools.translate import _
import openerp
from openerp import SUPERUSER_ID

class ove_structure(osv.osv):
    _name = 'ove.structure'
    _description = 'Structures de OVE'
    
    _columns = {
        'name': fields.char('Nom', required=True),
        'identifiant': fields.char('Identifiant structure', required=True),
        'users_line': fields.one2many('ove.structure.professionnel', 'structure_id', 'Professionnels'), 
    }
    
    def write(self, cr, uid, ids, vals, context=None):
        res = super(ove_structure, self).write(cr, uid, ids, vals, context=context)
        if 'users_line' in vals and vals['users_line']:
            api_obj = self.pool.get('is_api')
            usagers = api_obj.get_usagers_structure(cr, uid, ids[0], context)
            print 'usagers *****', usagers
            if usagers:
                for usager_id in usagers:
                    usager = self.pool.get('is.usager').browse(cr, uid, usager_id, context=context)
                    users = api_obj.get_users_usager(cr, uid, usager.structures_line, context=context)
                    api_obj.update_usager_groupes(cr, SUPERUSER_ID, usager_id, users, context=context)
        return res

    
class ove_structure_professionnel(osv.osv):
    _name = 'ove.structure.professionnel'
    _description = 'Utilsateurs liés aux groupes de structure'
    
    _columns = {
        'structure_id': fields.many2one('ove.structure', 'structure'),
        'user_id': fields.many2one('res.users', 'Professionnel', required=True),
        'group_1': fields.boolean('Groupe Impression'),
        'group_2': fields.boolean('Groupe Donnée Administrative'),
        'group_3': fields.boolean('Groupe Donnée Administrative Modification'),
        'group_4': fields.boolean('Groupe Donnée Institutionnelle'),
        'group_5': fields.boolean('Groupe Donnée Institutionnelle Modification'),
        'group_6': fields.boolean('Groupe Donnée Institutionnelle Validation'),
        'group_7': fields.boolean('Groupe Donnée métier'),
        'group_8': fields.boolean('Groupe Donnée métier Modification'),
        'group_9': fields.boolean('Groupe Donnée métier Validation'),
    }
    
    
class ove_usager_structure(osv.osv):
    _name = 'ove.usager.structure'
    _description = 'Les structures des usagers'
    
    _columns = {
        'usager_id': fields.many2one('is.usager', 'usager'),
        'structure_id': fields.many2one('ove.structure', 'Structure', required=True, ondelete='cascade'),
        'group_1': fields.boolean('Groupe Impression'),
        'group_2': fields.boolean('Groupe Donnée Administrative'),
        'group_3': fields.boolean('Groupe Donnée Administrative Modification'),
        'group_4': fields.boolean('Groupe Donnée Institutionnelle'),
        'group_5': fields.boolean('Groupe Donnée Institutionnelle Modification'),
        'group_6': fields.boolean('Groupe Donnée Institutionnelle Validation'),
        'group_7': fields.boolean('Groupe Donnée métier'),
        'group_8': fields.boolean('Groupe Donnée métier Modification'),
        'group_9': fields.boolean('Groupe Donnée métier Validation'),
    }


class ove_usager(osv.osv):
    _inherit = 'is.usager'
    
    _columns = {    
        'structures_line': fields.one2many('ove.usager.structure', 'usager_id', 'Structures'),
        'group_1': fields.many2one('ove.groupe', 'Groupe Impression', readonly=True),
        'group_2': fields.many2one('ove.groupe', 'Groupe Donnée Administrative', readonly=True),
        'group_3': fields.many2one('ove.groupe', 'Groupe Donnée Administrative Modification', readonly=True),
        'group_4': fields.many2one('ove.groupe', 'Groupe Donnée Institutionnelle', readonly=True),
        'group_5': fields.many2one('ove.groupe', 'Groupe Donnée Institutionnelle Modification', readonly=True),
        'group_6': fields.many2one('ove.groupe', 'Groupe Donnée Institutionnelle Validation', readonly=True),
        'group_7': fields.many2one('ove.groupe', 'Groupe Donnée métier', readonly=True),
        'group_8': fields.many2one('ove.groupe', 'Groupe Donnée métier Modification', readonly=True),
        'group_9': fields.many2one('ove.groupe', 'Groupe Donnée métier Validation', readonly=True),
        'group_10': fields.many2one('ove.groupe', 'Groupe Structure', readonly=True),    
    }  
    
    def create(self, cr, uid, vals, context=None):
        """ Créer les groupes associés à cet usager
        """
        new_id = super(ove_usager, self).create(cr, uid, vals, context=context)
        usager = self.browse(cr, uid, new_id, context=context)
        
        api_obj = self.pool.get('is_api')
        print 'structure_lines *****', usager.structures_line
        users = api_obj.get_users_usager(cr, uid, usager.structures_line, context=context)
        api_obj.create_ove_groups(cr, SUPERUSER_ID, 'Usager' + str(new_id), users, new_id, context=context)
        return new_id
    
    
    def write(self, cr, uid, ids, vals, context=None):
        """ 
            Mettre à jour les utilisateurs des groupes
        """
        res = super(ove_usager, self).write(cr, uid, ids, vals, context=context)
        api_obj = self.pool.get('is_api')
        #=======================================================================
        # """ Traiter les groupes manquant """
        # groups = api_obj.get_usager_groups(cr, uid, ids[0], context=context)
        # missed_groups = api_obj.get_missed_ove_group(cr, uid, groups, context=context)
        # if missed_groups:
        #     for group in missed_groups:
        #         api_obj.create_missed_ove_group(cr, uid, group, ids[0], 'Usager' + str(ids[0]), context=context)
        #=======================================================================
        
        """ Mettre à jours les utilisateurs des groupes """    
        if 'structures_line' in vals and vals['structures_line']:
            usager = self.browse(cr, uid, ids[0], context=context)
            users = api_obj.get_users_usager(cr, uid, usager.structures_line, context=context)
            api_obj.update_usager_groupes(cr, SUPERUSER_ID, ids[0], users, context=context)
        return res
    
    def unlink(self, cr, uid, ids, context=None):
        """  Si je supprime un usager, il faudrait supprimer ses groupes
        """        
        res = super(ove_usager, self).unlink(cr, uid, ids, context=context)
        
        group_obj = self.pool.get('ove.groupe')
        group_ids = group_obj.search(cr, uid, [('name','like','Usager' + str(ids[0])), ('usager_id','=',False)], context=context)
        group_obj.unlink(cr, SUPERUSER_ID, group_ids, context=context)
        return res


 
