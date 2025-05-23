from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, service_pb2, resources_pb2

YOUR_API_KEY = 'YOUR_CLARIFAI_API_KEY'

def detect_food_with_clarifai(image_path):
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', f'Key {YOUR_API_KEY}'),)

    with open(image_path, "rb") as f:
        file_bytes = f.read()

    request = service_pb2.PostModelOutputsRequest(
        model_id='food-item-recognition',
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=resources_pb2.Image(base64=file_bytes)))
        ])

    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != 0:
        print("Error:", response.status.description)
        return None

    concepts = response.outputs[0].data.concepts
    return concepts[0].name
