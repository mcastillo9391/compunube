import numpy as np
np.bool = bool

from gluoncv.model_zoo import get_model
from mxnet import nd
from mxnet.gluon.data.vision import transforms
from PIL import Image
import flask
import io

app = flask.Flask(__name__)

# cargar modelo una sola vez
net = get_model('cifar_resnet20_v1', classes=10)
net.load_parameters("net.params")

# nombres de las clases de CIFAR10
class_names = [
    'airplane', 'automobile', 'bird', 'cat', 'deer',
    'dog', 'frog', 'horse', 'ship', 'truck'
]

# transformaciones de imagen
transform_fn = transforms.Compose([
    transforms.Resize(32),
    transforms.CenterCrop(32),
    transforms.ToTensor(),
    transforms.Normalize(
        [0.4914,0.4822,0.4465],
        [0.2023,0.1994,0.2010]
    )
])

@app.route("/predict", methods=["POST"])
def predict():

    if flask.request.files.get("img"):

        # abrir y transformar la imagen
        img = Image.open(io.BytesIO(flask.request.files["img"].read()))
        img = transform_fn(nd.array(img))

        # obtener predicciones
        pred = net(img.expand_dims(axis=0))

        # convertir logits a probabilidades
        prob = nd.softmax(pred)

        # obtener índice de la clase con mayor probabilidad
        ind = nd.argmax(prob, axis=1).astype('int')
        prediction = class_names[ind.asscalar()]

        # obtener la probabilidad de la clase predicha
        probability = float(prob[0][ind.asscalar()].asscalar())

        return {"prediction": prediction, "probability": probability}

    return {"error": "no image received"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)