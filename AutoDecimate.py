import bpy

# 削減比率の指定
decimate_ratio = 0.8

# 削減後のTris値
decimated_tris = 0

# Thanks for these great site!
# https://bluebirdofoz.hatenablog.com/entry/2020/01/02/214529
# https://bluebirdofoz.hatenablog.com/entry/2019/06/13/085827 (object.children)
# https://bluebirdofoz.hatenablog.com/entry/2020/01/05/112942 (object.join)
# https://blenderartists.org/t/newbie-question-about-statistics/1291515/2
# https://blenderartists.org/t/getting-triangle-count-from-python/580809 (tris count)
# https://blenderartists.org/t/setting-origin-to-multiple-objects-via-script/1128140/6 (origin to geometory)

# 右記のURLで公開されている内容と同一です  :  https://bluebirdofoz.hatenablog.com/entry/2020/01/02/214529
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

# Scene全体のTrisなどを表示する
def countStatistics():
    view = bpy.context.scene.view_layers['View Layer']
    stats = bpy.context.scene.statistics(view) #returns string
    print(stats)

# 対象オブジェクトのTris数を集計
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

         #   decimated_tris+= countTris(obj)

#    print('After Decimated Tris:'+str(decimated_tris))

            #countTris(obj)

def scaling_mesh():
    for obj in bpy.context.view_layer.objects:
        if obj.type == 'MESH':
            obj.scale=10,10,10
            obj.location= obj.location.x*10,obj.location.y*10,obj.location.z*10

def origin_to_geometry():
    bpy.ops.object.select_all(action='SELECT') 
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.ops.object.select_all(action='DESELECT') 


def delete_empty():
    for item in bpy.context.view_layer.objects:
        if item.type == 'EMPTY':
            bpy.data.objects.remove(item)

# 高さを0にする。walkthroughに限定するならあった方が良い。ただし、実際の建物の建っている高さは変わってしまう
def alignment_position():
    for obj in bpy.context.view_layer.objects:
        if obj.type == 'MESH':
            obj.location.z=0

# 確認中のためコメントアウト
#def check_all_area_of_mesh():
#     for obj in bpy.context.view_layer.objects:
#        if obj.type == 'MESH':
#            obj.position.x

#メモ
#実行前に全てを非選択にする処理を追加する

# 実行
# 0. 全選択状態だとBlenderが落ちることがあるので、全て非選択にする
bpy.ops.object.select_all(action='DESELECT') 
# 1. importされたemptyの中にあるmeshを結合する
joinMesh()

# 4. meshの親オブジェクトになっているemptyを全て削除する
# emptyを削除するとメッシュが崩れてしまうため、いったんコメントアウトしておく
#delete_empty()

# 5. scaleを10に変更
scaling_mesh()

# 3. それぞれのmeshの座標をorigin to geometoryする
origin_to_geometry()

#countStatistics()
# 2. それぞれのemptyの中にあるmeshをdecimateする
decimate_mesh()

# zを0にする。
alignment_position()



print("finished")
