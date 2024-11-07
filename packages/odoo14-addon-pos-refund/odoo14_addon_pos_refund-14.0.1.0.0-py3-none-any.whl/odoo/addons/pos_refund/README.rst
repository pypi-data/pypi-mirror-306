.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
	:target: http://www.gnu.org/licenses/agpl
	:alt: License: AGPL-3

==========
Pos Refund
==========

This module allows to manage refunds from the POS frontend.


Installation
============

To install this module, you need to:

#. Just install.


Configuration
=============

To configure this module, you need to:

#. It is recommended to use a different sequence for Order Ref and Simplified Invoice Number.


Usage
=====

To use this module, you need to:

#. Click on Refund on the main POS screen.
#. Introduce the Order Ref or the Simplified Invoice Number.
#. Select the quantity of each product that needs to be refunded. It no quantity is defined or quantity is 0, the product will not be added to the refund order.
#. Click on 'Refund' button and complete the order.
#. NOTE: If a refund order has been created but it has to be ignored, click on Orders on the main POS screen and delete that specific order.


ROADMAP
=======

[ Enumerate known caveats and future potential improvements.
  It is mostly intended for end-users, and can also help
  potential new contributors discovering new features to implement. ]

* ...


Bug Tracker
===========

Bugs and errors are managed in `issues of GitHub <https://github.com/sygel-technology/sy-pos/issues>`_.
In case of problems, please check if your problem has already been
reported. If you are the first to discover it, help us solving it by indicating
a detailed description `here <https://github.com/sygel-technology/sy-pos/issues/new>`_.

Do not contact contributors directly about support or help with technical issues.


Credits
=======

Authors
~~~~~~~

* Manuel Regidor <manuel.regidor@sygel.es>


Contributors
~~~~~~~~~~~~

* Sygel
* Odoo Community Association (OCA)

Maintainer
~~~~~~~~~~

This module is maintained by Sygel.


This module is part of the `Sygel/sy-pos <https://github.com/sygel-technology/sy-pos>`_.

To contribute to this module, please visit https://github.com/sygel-technology.
