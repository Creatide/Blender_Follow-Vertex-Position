#------------------------------------------------------------
# Name:        FollowVertexPos
#
# Purpose:     Make empty to follow selected vertex.
# Author:      Sakari Niittymaa
#
# Created:     25.11.2012
# Copyright:   Copyright(c) 2016 Creatide / Sakari Niittymaa
#              http://www.creatide.com
#              hello@creatide.com
# Licence:     The MIT License (MIT)
#------------------------------------------------------------

import bpy

# Set active scene and object
activeScene = bpy.context.scene
currentObj = bpy.context.active_object

# Set custom empty name
emptyName = 'VertexTarget'

# Get selected vertex index number
vertexIndex = [i.index for i in bpy.context.active_object.data.vertices if i.select]

# Create empty
if emptyName not in bpy.data.objects:
    bpy.ops.object.empty_add(type='PLAIN_AXES')
    bpy.context.active_object.name = emptyName
targetEmpty = bpy.data.objects.get(emptyName)

# Run only if mesh is selected
if currentObj.type == 'MESH':

    # Loop current frame range
    for frame in range(activeScene.frame_end + 1):

        # Set active frame
        activeScene.frame_set(frame)

        # Make meshdata
        meshdata = currentObj.to_mesh( scene=activeScene, apply_modifiers=True, settings='PREVIEW' )

        # Loop meshdata vertices
        for vertex in meshdata.vertices:

            # Selected vertex only
            if vertex.index == vertexIndex[0]:

                # Calculate world coords for the empty
                newCoord = meshdata.vertices[vertex.index].co
                newCoord = currentObj.matrix_world * newCoord

                # Set new location for empty and make keyframe
                targetEmpty.location = newCoord
                targetEmpty.keyframe_insert(data_path='location', frame=(frame))

        # Remove meshdata data
        bpy.data.meshes.remove(meshdata)
else:
    print('SELECT MESH OBJECT!')
