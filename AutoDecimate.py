import bpy

# 削減比率の指定
decimate_ratio = 0.6

# 削減後のTris値
decimated_tris = 0

# Thanks for these great site!
# https://bluebirdofoz.hatenablog.com/entry/2020/01/02/214529
# https://bluebirdofoz.hatenablog.com/entry/2019/06/13/085827 (object.children)
# https://bluebirdofoz.hatenablog.com/entry/2020/01/05/112942 (object.join)
# https://blenderartists.org/t/newbie-question-about-statistics/1291515/2
# https://blenderartists.org/t/getting-triangle-count-from-python/580809 (tris count)


# 「ポリゴン数削減」モディファイアの反映
def apply_modifier_decimate(arg_objectname="Default", arg_ratio=1.0) -> bool:
    """「ポリゴン数削減」モディファイアの反映
    
    Keyword Arguments:
        arg_objectname {str} -- 対象オブジェクト名 (default: {"Default"})
        arg_ratio {float} -- 削減比率 (default: {1.0})

    Returns:
        bool -- 実行の正否
    """

    # 指定オブジェクトを取得する
    # (get関数は対象が存在しない場合 None が返る)
    targetob = bpy.data.objects.get(arg_objectname)

    # 指定オブジェクトが存在するか確認する
    if targetob == None:
        # 指定オブジェクトが存在しない場合は処理しない
        return False

    # 変更オブジェクトをアクティブに変更する
    bpy.context.view_layer.objects.active = targetob

    # 「ポリゴン数削減」モディファイアを追加する
    bpy.ops.object.modifier_add(type='DECIMATE')

    # 作成モディファイアを取得する
    selectmod = targetob.modifiers['Decimate']

    # 名前を指定オブジェクト名+「_Decimate」に設定する
    selectmod.name = arg_objectname + '_Decimate'

    # 削減設定を「束ねる」に設定する
    selectmod.decimate_type = 'COLLAPSE'

    # 比率を設定する
    selectmod.ratio = arg_ratio

    # 三角面化の実行を有効に設定する
    selectmod.use_collapse_triangulate = True

    # モディファイアを反映する
    bpy.ops.object.modifier_apply( modifier = arg_objectname + '_Decimate' )
  
    return True

def joinMesh():
    for item in bpy.context.view_layer.objects:
        if item.type == 'EMPTY':
            child_objs = item.children
            for child_obj in child_objs:
                if child_obj.type == 'MESH':
                    child_obj.select_set(True)
                    bpy.context.view_layer.objects.active = child_obj
                else:
                    child_obj.select_set(False) 
            bpy.ops.object.join()
            bpy.ops.object.select_all(action='DESELECT') 
            print(item.name)
    return 0

def countStatistics():
    view = bpy.context.scene.view_layers['View Layer']
    stats = bpy.context.scene.statistics(view) #returns string
    print(stats)

def countTris(obj):
    mesh = obj.data
    tri_count = 0
    for poly in mesh.polygons:
        if len(poly.vertices) == 3:
            tri_count += 1
    
    print(tri_count)
    return tri_count

def decimate_mesh(decimated_tris = 0):
    for obj in bpy.context.view_layer.objects:
    
        if obj.type == 'MESH':
            # ポリゴン数削減処理を行う
            apply_modifier_decimate(obj.name,decimate_ratio)
            # １つ処理し終わったときのstatisticsを表示
        #  countStatistics()
         #   decimated_tris+= countTris(obj)

#    print('After Decimated Tris:'+str(decimated_tris))

            #countTris(obj)

def scaling_mesh():
    for obj in bpy.context.view_layer.objects:
        if obj.type == 'MESH':
            obj.scale=100,100,100
            # 変更後の値をデフォルトとする
            obj.transform_apply(location=True, rotation=True, scale=True)



def delete_empty():
    for item in bpy.context.view_layer.objects:
        if item.type == 'EMPTY':
            bpy.data.objects.remove(item)


def decimate(obj,limit_num):
    bpy.context.view_layer.objects.active = obj
    #bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.ops.object.modifier_add(type='DECIMATE')

    #decim = bpy.context.object.modifiers["Decimate"]
    decim = bpy.context.view_layer.objects.modifiers["Decimate"]
    decim.decimate_type = 'DISSOLVE'
    decim.delimit = {'NORMAL'}
    decim.angle_limit = limit_num


# 実行
# 1. importされたemptyの中にあるmeshを結合する
joinMesh()
countStatistics()
# 2. それぞれのemptyの中にあるmeshをdecimateする
#decimate_mesh()

# 3. meshの親オブジェクトになっているemptyを全て削除する
delete_empty()

# 4. scaleを100に変更してからapplyする
scaling_mesh()

