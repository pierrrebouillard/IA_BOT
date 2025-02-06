import os
os.environ["CHROMA_DISABLE_TELEMETRY"] = "true"
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

from utils.vector_store import load_vector_store
import time

print("Début de load_vector_store()")
start = time.time()
vs = load_vector_store()
end = time.time()
print("load_vector_store() a retourné :", vs)
print("Temps écoulé :", end - start, "secondes")