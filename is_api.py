# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _

class is_api(osv.osv):
    _name = 'is_api'
    _description = u'Fonctions générales'
              
    def get_usagers_structure(self, cr, uid, structure_id, context=None):
        """ Retourner la liste des usagers appartenants à la structure passée en paramètre
        """
        usager_line_obj = self.pool.get('ove.usager.structure')
        line_ids = usager_line_obj.search(cr, uid, [('structure_id','=',structure_id)], context=context)
        print 'line_ids *****', line_ids
        usagers = list(set([line['usager_id'][0] for line in usager_line_obj.read(cr, uid, line_ids, ['usager_id'], context=context)]))   
        return usagers
    
    def get_usager_groups(self, cr, uid, usager_id, context=None):
        """ Retourner les groupes associés à l'usager passé en paramètre
        """
        group_obj = self.pool.get('ove.groupe')
        group_ids = group_obj.search(cr, uid, [('usager_id','=', usager_id)], context=context)
        groups = []
        for group in group_obj.read(cr, uid, group_ids, ['id', 'code'], context=context):
            groups.append({'id':group['id'], 'code':group['code']})
        
        newlist = sorted(groups, key=lambda k: k['code'])
        return newlist
        
                   
    def get_users_usager(self, cr, uid, structure_lines, context=None):
        """ Retourner les utilisateurs liés aux groupes de l'usager à partir des structures qui leurs appartient
        """
        users = {'group_1':[], 'group_2':[], 'group_3':[], 'group_4':[], 'group_5':[],
                 'group_6':[], 'group_7':[], 'group_8':[], 'group_9':[], 'group_10':[]
                }
        if not structure_lines:
            return users
        for line in structure_lines:
            if line.structure_id.users_line:
                for user_line in  line.structure_id.users_line:
                    if user_line.group_1 and line.group_1:
                        users['group_1'].append(user_line.user_id.id)
                        users['group_10'].append(user_line.user_id.id)
                    if user_line.group_2 and line.group_2:
                        users['group_2'].append(user_line.user_id.id)
                        users['group_10'].append(user_line.user_id.id)
                    if user_line.group_3 and line.group_3:
                        users['group_3'].append(user_line.user_id.id)
                        users['group_10'].append(user_line.user_id.id)
                    if user_line.group_4 and line.group_4:
                        users['group_4'].append(user_line.user_id.id)
                        users['group_10'].append(user_line.user_id.id)
                    if user_line.group_5 and line.group_5:
                        users['group_5'].append(user_line.user_id.id)
                        users['group_10'].append(user_line.user_id.id)
                    if user_line.group_6 and line.group_6:
                        users['group_6'].append(user_line.user_id.id)
                        users['group_10'].append(user_line.user_id.id)
                    if user_line.group_7 and line.group_7:
                        users['group_7'].append(user_line.user_id.id)
                        users['group_10'].append(user_line.user_id.id)
                    if user_line.group_8 and line.group_8:
                        users['group_8'].append(user_line.user_id.id)
                        users['group_10'].append(user_line.user_id.id)
                    if user_line.group_9 and line.group_9:
                        users['group_9'].append(user_line.user_id.id)
                        users['group_10'].append(user_line.user_id.id)
            """ Eliminer les doublons des listes """
            users.update({'group_1': list(set(users['group_1']))})
            users.update({'group_2': list(set(users['group_2']))})
            users.update({'group_3': list(set(users['group_3']))})
            users.update({'group_4': list(set(users['group_4']))})
            users.update({'group_5': list(set(users['group_5']))})
            users.update({'group_6': list(set(users['group_6']))})
            users.update({'group_7': list(set(users['group_7']))})
            users.update({'group_8': list(set(users['group_8']))})
            users.update({'group_9': list(set(users['group_9']))})
            users.update({'group_10': list(set(users['group_10']))})
        return users
                        
    
    def create_group(self, cr, uid, code_groupe, prefix, name_group, users, usager_id, context=None):
        """ Création d'un groupe OVE
        """
        vals = {
            'code': code_groupe,
            'name': prefix + ' - ' + name_group,
            'user_ids': [[6, 0, users]],
            'usager_id': usager_id,
        }
        return self.pool.get('ove.groupe').create(cr, uid, vals, context=context)
    
    def associate_groupe_usager(self, cr, uid, usager_id, group_id, group_usager, context=None):
        """ Associer un groupe au groupe correspondant de l'usager
        """
        usager_obj = self.pool.get('is.usager')
        if group_usager == 'G1':
            usager_obj.write(cr, uid, usager_id, {'group_1': group_id}, context=context)
        if group_usager == 'G2':
            usager_obj.write(cr, uid, usager_id, {'group_2': group_id}, context=context)
        if group_usager == 'G3':
            usager_obj.write(cr, uid, usager_id, {'group_3': group_id}, context=context)
        if group_usager == 'G4':
            usager_obj.write(cr, uid, usager_id, {'group_4': group_id}, context=context)
        if group_usager == 'G5':
            usager_obj.write(cr, uid, usager_id, {'group_5': group_id}, context=context)
        if group_usager == 'G6':
            usager_obj.write(cr, uid, usager_id, {'group_6': group_id}, context=context)
        if group_usager == 'G7':
            usager_obj.write(cr, uid, usager_id, {'group_7': group_id}, context=context)
        if group_usager == 'G8':
            usager_obj.write(cr, uid, usager_id, {'group_8': group_id}, context=context)
        if group_usager == 'G9':
            usager_obj.write(cr, uid, usager_id, {'group_9': group_id}, context=context)
        if group_usager == 'G10':
            usager_obj.write(cr, uid, usager_id, {'group_10': group_id}, context=context)
        return True
        
    def create_ove_groups(self, cr, uid, prefix, users, usager_id, context=None):
        """ Création de l'ensemble des groupes pour chaque usager ou structure 
        """
        group_id = self.create_group(cr, uid, 'G1', prefix, 'Groupe Impression', users['group_1'], usager_id, context=context)
        self.associate_groupe_usager(cr, uid, usager_id, group_id, 'G1', context)
        
        group_id = self.create_group(cr, uid, 'G2', prefix, 'Groupe Donnée Administrative', users['group_2'], usager_id, context=context)
        self.associate_groupe_usager(cr, uid, usager_id, group_id, 'G2', context)
        
        group_id = self.create_group(cr, uid, 'G3', prefix, 'Groupe Donnée Administrative Modification', users['group_3'], usager_id, context=context)
        self.associate_groupe_usager(cr, uid, usager_id, group_id, 'G3', context)
        
        group_id = self.create_group(cr, uid, 'G4', prefix, 'Groupe Donnée Institutionnelle', users['group_4'], usager_id, context=context)
        self.associate_groupe_usager(cr, uid, usager_id, group_id, 'G4', context)
        
        group_id = self.create_group(cr, uid, 'G5', prefix, 'Groupe Donnée Institutionnelle Modification', users['group_5'], usager_id, context=context)
        self.associate_groupe_usager(cr, uid, usager_id, group_id, 'G5', context)
        
        group_id = self.create_group(cr, uid, 'G6', prefix, 'Groupe Donnée Institutionnelle Validation', users['group_6'], usager_id, context=context)
        self.associate_groupe_usager(cr, uid, usager_id, group_id, 'G6', context)
        
        group_id = self.create_group(cr, uid, 'G7', prefix, 'Groupe Donnée métier', users['group_7'], usager_id, context=context)
        self.associate_groupe_usager(cr, uid, usager_id, group_id, 'G7', context)
        
        group_id = self.create_group(cr, uid, 'G8', prefix, 'Groupe Donnée métier Modification', users['group_8'], usager_id, context=context)
        self.associate_groupe_usager(cr, uid, usager_id, group_id, 'G8', context)
        
        group_id = self.create_group(cr, uid, 'G9', prefix, 'Groupe Donnée métier Validation', users['group_9'], usager_id, context=context)
        self.associate_groupe_usager(cr, uid, usager_id, group_id, 'G9', context)
        
        group_id = self.create_group(cr, uid, 'G10', prefix, 'Groupe Structure', users['group_10'], usager_id, context=context)
        self.associate_groupe_usager(cr, uid, usager_id, group_id, 'G10', context)
        return True
    
    def update_usager_groupes(self, cr, uid, usager_id, users, context=None):
        """ Mettre à jour les groupes de l'usager courant
        """
        groups = self.get_usager_groups(cr, uid, usager_id, context=context)
        for group in groups:
            if group['code'] == 'G1':
                self.update_ove_group(cr, uid, group['id'], users['group_1'], context)
            if group['code'] == 'G2':
                self.update_ove_group(cr, uid, group['id'], users['group_2'], context)
            if group['code'] == 'G3':
                self.update_ove_group(cr, uid, group['id'], users['group_3'], context)
            if group['code'] == 'G4':
                self.update_ove_group(cr, uid, group['id'], users['group_4'], context)
            if group['code'] == 'G5':
                self.update_ove_group(cr, uid, group['id'], users['group_5'], context)
            if group['code'] == 'G6':
                self.update_ove_group(cr, uid, group['id'], users['group_6'], context)
            if group['code'] == 'G7':
                self.update_ove_group(cr, uid, group['id'], users['group_7'], context)
            if group['code'] == 'G8':
                self.update_ove_group(cr, uid, group['id'], users['group_8'], context)
            if group['code'] == 'G9':
                self.update_ove_group(cr, uid, group['id'], users['group_9'], context)
            if group['code'] == 'G10':
                self.update_ove_group(cr, uid, group['id'], users['group_10'], context)
        return True    
            
    def update_ove_group(self, cr, uid, group_id, users, context=None):
        """ Mettre à jour d'un groupe d'un usager
        """
        vals = {
            'user_ids': [[6, 0, users]],
        }
        return self.pool.get('ove.groupe').write(cr, uid, group_id, vals, context=context)
            
    def get_missed_ove_group(self, cr, uid, usager_groups, context=None):
        """ Chercher le groupe manquant dans la liste des groupes d'un usager
        """
        groups = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10']
        exist_groups = []
        missed_groups = []
        for group in usager_groups:
            exist_groups.append(group['code'])
        for group in groups:
            if group not in exist_groups:
                missed_groups.append(group)
            else:
                continue
        return missed_groups
    
    def create_missed_ove_group(self, cr, uid, group, usager_id, prefix, context=None):
        """ Créer les groupes manquant de l'usager passé en paramètre
        """
        if group == 'G1':
            self.create_group(cr, uid, 'G1', prefix, 'Groupe Impression', [], usager_id, context=context)
        if group == 'G2':
            self.create_group(cr, uid, 'G2', prefix, 'Groupe Donnée Administrative', [], usager_id, context=context)
        if group == 'G3':
            self.create_group(cr, uid, 'G3', prefix, 'Groupe Donnée Administrative Modification', [], usager_id, context=context)
        if group == 'G4':
            self.create_group(cr, uid, 'G4', prefix, 'Groupe Donnée Institutionnelle', [], usager_id, context=context)
        if group == 'G5':
            self.create_group(cr, uid, 'G5', prefix, 'Groupe Donnée Institutionnelle Modification', [], usager_id, context=context)
        if group == 'G6':
            self.create_group(cr, uid, 'G6', prefix, 'Groupe Donnée Institutionnelle Validation', [], usager_id, context=context)
        if group == 'G7':
            self.create_group(cr, uid, 'G7', prefix, 'Groupe Donnée métier', [], usager_id, context=context)
        if group == 'G8':
            self.create_group(cr, uid, 'G8', prefix, 'Groupe Donnée métier Modification', [], usager_id, context=context)
        if group == 'G9':
            self.create_group(cr, uid, 'G9', prefix, 'Groupe Donnée métier Validation', [], usager_id, context=context)
        if group == 'G10':
            self.create_group(cr, uid, 'G10', prefix, 'Groupe Structure', [], usager_id, context=context)      
        return True
            