
        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 20px;">
                        <i>f({self.variable_1_display})</i> = 
                    </td>
                    
                    <td valign="middle" style="padding-right: 10px;">
                        <table cellpadding="0" cellspacing="0" style="font-size: 36px;">
                            <tr>
                                <td align="center" style="border-bottom: 3px solid currentColor; padding: 0px 10px 4px 10px;">
                                    1
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 4px 10px 0px 10px;">
                                    &radic;<span style="text-decoration: overline;">2&pi;</span>
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 5px;">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td valign="center" style="font-size: 51px; padding-right: 0px;">
                                    <i>e</i>
                                </td>
                                <td valign="top" style="padding-bottom: 28px; padding-left: 2px;">
                                    <table cellpadding="0" cellspacing="0" style="font-size: 30px;">
                                        <tr>
                                            <td rowspan="2" valign="middle" style="padding-right: 4px; font-size: 25px;">
                                                &minus;
                                            </td>
                                            <td align="center" style="border-bottom: 2px solid currentColor; padding: 0px 2px 1px 2px;">
                                                {self.variable_1_display}<sup>2</sup>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center" style="padding: 1px 2px 0px 2px;">
                                                2
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 25px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

 