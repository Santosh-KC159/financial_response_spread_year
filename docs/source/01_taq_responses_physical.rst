.. _taq_responses_physical:

TAQ Responses Physical
**********************

The objective of this part of the code is to reproduce the sections 3.1 and 3.2
of the paper `Cross–response in correlated financial markets:  individual
stocks
<https://link.springer.com/content/pdf/10.1140/epjb/e2016-60818-y.pdf>`_.

All the results obtained with the **TAQ Responses Physical** module are the
base to the other implementations (:ref:`taq_physical_shift`,
:ref:`taq_responses_physical_shift`, :ref:`taq_responses_trade`,
:ref:`taq_trade_shift`, :ref:`taq_responses_trade_shift`,
:ref:`taq_responses_activity`, :ref:`taq_responses_physical_short_long`,
:ref:`taq_avg_spread`, :ref:`taq_avg_responses_physical` and
:ref:`taq_statistics`).

Run the code
============

To run the code, please follow the instructions of the README.md in the
`GitHub <https://github.com/juanhenao21/financial_response_spread_year>`_
repository.

Modules
=======
The code is divided in four parts:
    * `Tools`_: some functions for repetitive actions.
    * `Analysis`_: code to analyze the data.
    * `Plot`_: code to plot the data.
    * `Main`_: code to run the implementation.

Tools
-----
.. automodule:: taq_data_tools_responses_physical
   :members:

Analysis
--------
.. automodule:: taq_data_analysis_responses_physical
   :members:

Plot
----
.. automodule:: taq_data_plot_responses_physical
   :members:

Main
----
.. automodule:: taq_data_main_responses_physical
   :members:
