#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Atan function voor Sym Express 3

    Copyright (C) 2024 Gien van den Enden - swvandenenden@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""

import cmath

from symexpress3         import symexpress3
from symexpress3.symfunc import symTrigonometricData
from symexpress3.symfunc import symFuncTrigonoBase

class SymFuncAtan( symFuncTrigonoBase.SymFuncTrigonoBase ):
  """
  Atan function
  """
  def __init__( self ):
    super().__init__()
    self._name      = "atan"
    self._desc      = "atan"
    self._minparams = 1    # minimum number of parameters
    self._maxparams = 1    # maximum number of parameters
    self._syntax    = "atan(<x>)"


  def functionToValue( self, elem ):

    def _conversTable( elem ):
      funcname = None
      if elem.name == 'atan':
        funcname = 'tan'

      if funcname == None:
        return None

      exp = elem.elements[ 0 ]

      # print( "funcname: {}, exp: {}, type: {}".format( funcname, str( exp ), type( exp ) ))

      for tri in symTrigonometricData.trigonometricdata:

        if tri[ 0 ] != funcname:
          continue

        # convert string to expression
        if tri[ 5 ] == None:
          tri[ 5 ] = symexpress3.SymFormulaParser( tri[ 4 ] )
          tri[ 5 ].optimizeNormal()
          if tri[ 5 ].numElements() == 1:
            tri[ 5 ] = tri[ 5 ].elements[ 0 ]

        # print( "found {}, expr: {}, type: {}".format( tri[ 0 ], str( tri[ 5 ] ), type( tri[5] ) ) )

        if not exp.isEqual( tri[ 5 ] ):
          continue

        # found one
        angle = ''
        if tri [ 1 ] == -1:
          angle += '-1 '

        angle += str( tri[ 2 ] ) + ' / ' + str( tri[ 3 ] ) + ' * pi '

        newelem = symexpress3.SymFormulaParser( angle )
        newelem.powerSign        = elem.powerSign
        newelem.powerCounter     = elem.powerCounter
        newelem.powerDenominator = elem.powerDenominator

        return newelem

      return None

    if self._checkCorrectFunction( elem ) != True:
      return None

    result = _conversTable( elem )
    if result != None:
      return result

    # atan( -x ) = -atan( x )
    result = self._convertSinCosTanAtanSign( elem )
    if result != None:
      return result

    return None


  def _getValueSingle( self, dValue, dValue2 = None ):
    return cmath.atan( dValue )



#
# Test routine (unit test), see testsymexpress3.py
#
def Test( display = False):
  """
  Unit test
  """
  def _Check(  testClass, symTest, value, dValue, valueCalc, dValueCalc ):
    if display == True :
      print( f"naam    : {testClass.name}" )
      print( f"function: {str( symTest )}" )
      print( f"Value   : {str( value   )}" )
      print( f"DValue  : {str( dValue  )}" )

    if str( value ) != valueCalc or dValue != dValueCalc:
      print( f"Error unit test {testClass.name} function" )
      raise NameError( f'function {testClass.name}, unit test error: {str( symTest )}, value: {value}' )

  symTest = symexpress3.SymFormulaParser( 'atan( 1 )' )
  symTest.optimize()
  testClass = SymFuncAtan()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, round( dValue, 10), "1 * 4^^-1 * pi", round( 0.7853981633974483, 10) )


  symTest = symexpress3.SymFormulaParser( 'atan( -2 )' )
  symTest.optimize()
  testClass = SymFuncAtan()
  value     = testClass.functionToValue( symTest.elements[ 0 ] )
  dValue    = testClass.getValue(        symTest.elements[ 0 ] )

  _Check(  testClass, symTest, value, round( dValue, 10), "(-1) *  atan( 2 )", round( -1.1071487177940904, 10) )


if __name__ == '__main__':
  Test( True )
