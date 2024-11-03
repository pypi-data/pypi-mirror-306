Libpulse API
============

libpulse module
---------------
Overview
""""""""
To use libpulse import the libpulse module from the libpulse package, start the
asyncio event loop, instantiate the LibPulse class by running it as an async
context manager. The LibPulse instance connects to the Pulseaudio or Pipewire
server and one is ready to invoke pulse async functions or non-async
functions.

Async functions are those pulse functions that return results through a
callback. They are implemented by methods of the LibPulse instance that are
asyncio coroutines. They have the same name as the corresponding pulse async
function.

Non-async functions have their corresponding ctypes foreign functions defined in
the libpulse module namespace under the same name as the corresponding pulse
function. They may be called directly once the LibPulse class has been
instantiated.

Libpulse functions, structures and enums are documented by the  `PulseAudio
Documentation`_

Module attributes
"""""""""""""""""
- All the constants that are defined by enums in the pulse headers (see the
  pulse_enums module).
- The following constants defined in the headers as macros:

    + PA_INVALID_INDEX
    + PA_VOLUME_NORM
    + PA_VOLUME_MUTED
    + PA_VOLUME_MAX
    + PA_VOLUME_INVALID
    + PA_CHANNELS_MAX

- All the pulse functions (async and non-async) whose signature is defined by
  the pulse headers and that are not callbacks (that is, all the keys in the
  ``signatures`` dictionary of the pulse_functions module).
- CTX_STATES, EVENT_FACILITIES, EVENT_TYPES dictionaries that map values to
  their symbolic names.
- ``struct_ctypes`` a dictionary mapping the name of each pulse structure
  defined by the pulse headers (see the pulse_structs module) to the
  corresponding ctypes subclass of ``Structure``.

LibPulse class
--------------
Constructor
"""""""""""
class libpulse.LibPulse(name, server=None, flags=PA_CONTEXT_NOAUTOSPAWN)

Parameters:
  - ``name`` application name passed to pa_context_new() upon invocation.
  - ``server`` and ``flags`` are passed to pa_context_connect() upon invocation,
    see the `PulseAudio Documentation`_.

LibPulse is an async context manager connecting to the PulseAudio or Pipewire
server when it is entered. It must be instanciated this way:

.. code-block:: python

    import asyncio
    from libpulse.libpulse import LibPulse

    async def main():
        async with LibPulse('my libpulse') as lib_pulse:
            ...

    asyncio.run(main())



Instance attributes
"""""""""""""""""""
``c_context``
  The ctypes pa_context opaque pointer used as the first parameter of many pulse
  functions. It is required by some non-async functions as their first
  parameter. It is never used when invoking the LibPulse coroutine methods
  (although the C pulse async function does).

``loop``
  The asyncio loop.

``state``
  The pulse context state. A tuple whose first element is one of the constants
  of the ``pa_context_state`` enum as a string. The second element is one of the
  constants of the ``pa_error_code`` enum as a string.

Async pulse functions as coroutines
"""""""""""""""""""""""""""""""""""
The pulse async functions are implemented as LibPulse methods that are
asyncio coroutines except for five :ref:`Not implemented` methods.

These methods are sorted in four lists according to their signature and the
signature of their callbacks. These lists are the LibPulse class attributes:

  - context_methods
  - context_success_methods
  - context_list_methods
  - stream_success_methods

Methods parameters
''''''''''''''''''
The type of the first parameter of the pulse async functions whose name
starts with ``pa_context`` is ``pa_context *``. This parameter is **omitted**
upon invocation of the corresponding LibPulse method (the Libpulse instance
already knows it as one of its attributes named ``c_context``).

The type of the penultimate parameter of the pulse async functions is the
type of the callback. This parameter is **omitted** upon invocation of the
corresponding LibPulse method as the Libpulse instance already knows this type
from the signature of the function in the ``pulse_functions`` module.

The type of the last parameter of the pulse async functions is ``void *``.
The parameter is meant to be used to match the  callback invocation with the
pulse function that triggered it when the implementation is done in C
language. This last parameter is not needed and **omitted** upon invocation of
the corresponding LibPulse method (the callback is implemented as an embedded
function in the method definition, more details at :ref:`Callbacks`).

For example pa_context_get_server_info() is invoked as:

.. code-block:: python

    server_info = await lib_pulse.pa_context_get_server_info()

Methods return value
''''''''''''''''''''
When one of the parameters of the callback of an async function is a pointer to
a pulse structure, the corresponding LibPulse coroutine method returns
a PulseStructure instance. See below.

The ``context_methods`` return an empty list if the callback has no other
parameter than ``pa_context *c`` and ``void *userdata``, they return a list if
the callback has set more than one of its parameters, otherwise they return the
unique parameter set by the callback.

The ``context_success_methods`` and ``stream_success_methods`` return an
``int``, either PA_OPERATION_DONE or PA_OPERATION_CANCELLED.
PA_OPERATION_CANCELLED occurs as a result of the context getting disconnected
while the operation is pending.

The ``context_list_methods`` return a list after the pulse library has
invoked repeatedly the callback. The callback is invoked only once for methods
whose name ends with ``_by_name``, ``_by_index``, ``_info`` or ``_formats`` and
the result returned by those coroutines in that case is this single element
instead of the list.

Other public methods
""""""""""""""""""""
coroutine ``get_current_instance()``
  A static method.

  Return the current LibPulse instance or None if it does not exist. There can
  only be one asyncio event loop per thread and consequently only one pulse loop
  running on the asyncio loop and one LibPulse instance per thread.

  Raises LibPulseStateError if the instance is not in the PA_CONTEXT_READY
  state.

coroutine ``get_events_iterator()``
  Return an Asynchronous Iterator of libpulse events. There can only be one such
  iterator at any given time.

  Use the iterator in an async for loop to loop over PulseEvent instances whose
  types have been selected by a previous call to the pa_context_subscribe()
  coroutine. pa_context_subscribe() may be called while the loop is running
  to change the kind of events one is interested about. The async for loop may
  be terminated by invoking the close() method of the iterator from within the
  loop or from another asyncio task.

.. _Not implemented:

Not implemented
"""""""""""""""
The following pulse async functions are not implemented as methods of a
LibPulse instance:

    pa_signal_new() and pa_signal_set_destroy():
        Signals are handled by asyncio and the hook signal support built into
        pulse abstract main loop is not needed.

For the following async functions, the callback has to be implemented  by the
user of the libpulse API:

  - pa_context_rttime_new()
  - pa_stream_write()
  - pa_stream_write_ext_free()

PulseEvent class
----------------
An instance of PulseEvent is returned by the async iterator returned by the
get_events_iterator() method of a LibPulse instance.

Its attributes are::

  facility:   str - name of the facility, for example 'sink'.
  index:      int - index of the facility.
  type:       str - type of event, 'new', 'change' or 'remove'.

PulseStructure class
--------------------
A PulseStructure instance is a deep copy of the pulse structure pointed to by
one of the parameters of a callback. The memory pointed to by the pointer is
short-lived, only valid during the execution of the callback, hence the need for
this construct.

The PulseStructure instance embeds PulseStructure instances for those of its
members that are nested pulse structures or pointers to other pulse structures
(recursively).

The attributes of the PulseStructure instance are the names of the members of
the pulse structure as listed in the pulse_structs module or the Pulseaudio
documentation.

Constructor
"""""""""""
class PulseStructure(c_struct, c_structure_type)

Parameters:
  - ``c_struct`` ctypes structure such as a ctypes pointer dereferenced using
    its ``contents`` attribute.
  - ``c_structure_type`` subclass of ctypes Structure corresponding to the type
    of the ``c_struct`` pointer. It is one of the values of the
    ``struct_ctypes`` dictionary.

PropList class
--------------
When the member of a pulse structure is a pointer to a ``proplist``, the
corresponding PulseStructure attribute is set to an instance of PropList
class. The PropList class is a subclass of ``dict`` and the elements of the
proplist can be accessed as the elements of a dictionary.

Building ctypes pulse structures
--------------------------------
The parameters of some non-async functions are pointers to pulse structures.
Here is an example showing how to build a pointer to the ``pa_sample_spec``
structure:

.. code-block:: python

   import ctypes as ct
   from libpulse.libpulse import struct_ctypes

   sample_spec = {'format': 3, 'rate': 44100, 'channels': 2}
   clazz = struct_ctypes['pa_sample_spec']

   # Instantiate clazz with (3, 44100, 2)
   struct = clazz(*sample_spec.values())

   # Using ctypes pointer() here to be able to print the pointer contents
   # below, but lightweight byref() is sufficient if only passing the pointer
   # to a function.
   pointer = ct.pointer(struct)

   # Print '<libpulse.libpulse_ctypes.pa_sample_spec object at 0xddddddd>'.
   print(pointer.contents)
   # Print '3'.
   print(pointer.contents.format)

Another way is to use the convenience classes Pa_buffer_attr, Pa_cvolume,
Pa_channel_map, Pa_format_info or Pa_sample_spec. In that case the above example
becomes:

.. code-block:: python

   pointer = Pa_sample_spec(*sample_spec.values()).byref()

`examples/pa_stream_new.py`_ shows how to create instances of two structures and
pass their pointers to ``pa_stream_new()``. The example shows also how to build
a PulseStructure from a pointer returned by ``pa_stream_get_sample_spec()``.

The ``pactl.py`` implementation uses the Pa_cvolume and Pa_channel_map classes
to build ctypes ``Structure`` instances and pass their pointer to some of the
`pactl.py non-async functions`_.

Auto-generated modules
----------------------
The ``libpulse_ctypes`` module uses the ``pulse_types``, ``pulse_enums``,
``pulse_structs`` and ``pulse_functions`` modules of the libpulse package to
build:

  - The libpulse ctypes foreign functions corresponding to the pulse
    functions.
  - The subclasses of the ctypes Structure corresponding to the pulse
    structures.
  - The constants of the enums of the pulse library.

These four modules are generated from the headers of the pulse library and
may be re-generated using ``gcc`` and ``pyclibrary`` as explained in the
:ref:`Development` section, although this is not necessary. The ABI of the
pulse library is pretty much stable and using recent versions of Pulseaudio
and Pipewire generates the same modules.

.. _`PulseAudio Documentation`:
   https://freedesktop.org/software/pulseaudio/doxygen/index.html
.. _examples/pa_stream_new.py:
   https://gitlab.com/xdegaye/libpulse/-/blob/master/examples/pa_stream_new.py?ref_type=heads#L1
.. _`pactl.py non-async functions`:
   https://gitlab.com/xdegaye/libpulse/-/blob/master/libpulse/pactl.py?ref_type=heads#L30
