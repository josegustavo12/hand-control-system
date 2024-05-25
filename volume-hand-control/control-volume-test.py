import pulsectl

pulse = pulsectl.Pulse('volume-control')
sinks = pulse.sink_list()

if sinks:
    sink = sinks[0]
    print(f"Dispositivo de saída atual: {sink.description}")

    current_volume = sink.volume.values[0]
    print(f"Volume atual: {current_volume * 100:.0f}%")

    new_volume = 0.5
    pulse.volume_set_all_chans(sink, new_volume)
    print(f"Volume definido para {new_volume * 100:.0f}%")

else:
    print("Nenhum dispositivo de saída de áudio encontrado.")

pulse.close()
