
        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 15px;">
                        t = 
                    </td>
                    
                    <td align="center">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid; padding: 0 10px 6px 10px;">
                                    {self.variable_5_display}
                                </td>
                            </tr>
                            
                            <tr>
                                <td align="center" >
                                    <table cellpadding="0" cellspacing="0" align="center">
                                        <tr>
                                            <td align="center" padding: 2px 8px 6px 8px;">
                                                {self.variable_6_display}&times;&radic;{self.variable_2_display}
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                    
                    <td valign="middle" style="padding-left: 20px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)
