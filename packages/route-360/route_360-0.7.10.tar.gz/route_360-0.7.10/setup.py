from setuptools import setup, find_packages

build_requires = [
    'pandas',
    'datasets',
    'sentence-transformers',
    'setfit==1.0.2',
    'onnx==1.14.0',
    'tqdm',
    'scikit-learn',
    'huggingface_hub',
    'accelerate',
    'ollama',
    'matplotlib',
    'chardet',
    'openai==1.37.1',
    'anthropic',
    'onnxconverter-common',
    'faiss-cpu',
]

route_requires = [
    'numpy==1.24.4',
    'tokenizers==0.19.1',
    'onnxruntime==1.15.1',
    'joblib==1.4.2',
]


setup(
    name='route-360',
    version='0.7.10',
    description='Low latency, High Accuracy, Custom Query routers for Humans and Agents',
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'build': build_requires,
        'route': route_requires,
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)